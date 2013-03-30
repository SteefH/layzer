import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

import beject


@beject.inject(
    feed='feed_model',
    feed_site='feed_site_model',
    subscription='subscription_model',
    discovery='feeddiscovery',
    datetime='datetime'
)
class SubscriptionService(object):

    class NoFeedException(Exception):
        """
        Exception raised when there's no feed found at a given url.
        """

    class AlreadySubscribedException(Exception):
        """
        Exception raised when the user is already subscribed to a given feed.
        """

    class DoesNotExistException(Exception):
        pass



    def _get_or_create_feed(self, url):
        """
        Get or create a feed model based on a given url. Try to discover
        the feed at the url when there's no feed model yet for the url
        """

        feed = site = None
        try:
            feed = self.feed.objects.get(feed_url=url)
        except self.feed.DoesNotExist:
            pass

        try:
            site = self.feed_site.objects.get(site_url=url)
            feed = site.feed
        except self.feed_site.DoesNotExist:
            pass

        if not feed and not site:
            logger.info('Attempting feed discovery at {0}'.format(url))
            try:
                name, site_url, feed_url = self.discovery.discover(url)
                logger.info('Feed found at {0}: {1}, {2}, {3}'.format(url, name, site_url, feed_url))
            except self.discovery.FeedException:
                raise self.NoFeedException
            feed, created = self.feed.objects.get_or_create(feed_url=feed_url)
            site, created = self.feed_site.objects.get_or_create(
                feed=feed, site_url=url
            )
            site.name = name
            site.save()
        return site, feed


    def add_subscription(self, url, user):
        site, feed = self._get_or_create_feed(url)
        try:
            sub = self.subscription.objects.get_by_feed_and_user(
                feed, user
            )
            if sub.deleted_on is not None:
                sub.deleted_on = None
            else:
                raise self.AlreadySubscribedException
        except self.subscription.DoesNotExist:
            sub = self.subscription(site=site, user=user, name=site.name)
        sub.save()
        return sub

    def remove_subscription(self, subscription):
        subscription.deleted_on = self.datetime.now()
        subscription.save()

    def get_all(self, user):
        s = self.subscription
        subs =  s.objects.filter_by_user(user).select_related('feed')
        return subs

    def get_subscription(self, feed_url, user):
        try:
            feed = self.feed.objects.get(feed_url=feed_url)
            return self.subscription.objects.get_by_feed_and_user(
                feed, user
            )
        except (self.feed.DoesNotExist, self.subscription.DoesNotExist):
            raise self.DoesNotExistException

    _editable_fields = ['name']

    def save_subscription(self, feed_url, data, user):
        obj = self.get_subscription(feed_url, user)

        for fieldname in self._editable_fields:
            if fieldname in data:
                setattr(obj, fieldname, data[fieldname])
        obj.save()
        return obj

    def delete_subscription(self, feed_url, user):
        obj = self.get_subscription(feed_url, user)
        obj.deleted_on = self.datetime.now()
        obj.save()


@beject.inject(
    'datetime',
    feed_item_status='feed_item_status_model'
)
class FeedItemStatusService(object):


    def _get_status(self, feed_item, user):
        return self.feed_item_status.objects.get_or_create(
            feed_item=feed_item, user=user
        )

    def mark_read(self, feed_item, user):
        status = self._get_status(feed_item, user)
        if status.read_on is not None:
            return

        status.read_on = self.datetime.now()
        status.kept_unread_on = None
        status.save()

    def star_item(self, feed_item, user):
        status = self._get_status(feed_item, user)
        status.starred_on = self.datetime.now()
        status.save()


@beject.inject(
    feed_item='feed_item_model',
    feed='feed_model'
)
class FeedService(object):

    def get_feed(self, feed_url):
        return self.feed.objects.get(feed_url=feed_url)

    def get_all(self):
        return self.feed.objects.all()

@beject.inject(
    feed_item='feed_item_model'
)
class FeedItemService(object):
    def add_or_update_item(self,
        feed, url, title, content, excerpt, published_on, author=None, author_link=None,
        author_email=None
    ):
        try:
            item = self.feed_item.objects.get(link=url, feed=feed)
        except self.feed_item.DoesNotExist:
            item = self.feed_item()
            item.link = url
            item.feed = feed
        item.title = title
        item.short_body = excerpt
        item.publisher = author
        item.body = content
        item.published_on = published_on
        item.save()
        return item

    def get_all(self, **filters):
        return self.feed_item.objects.filter(**filters)
