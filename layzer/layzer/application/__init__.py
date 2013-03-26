import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

import beject

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


    @classmethod
    def create_default(cls):
        """Create the default service
        """
        from layzer.application import models
        from layzer.util import feeddiscovery
        from datetime import datetime
        return cls(models.Feed, models.Subscription, feeddiscovery, datetime)

    @beject.inject
    def __init__(self, feed_model, feed_site_model, subscription_model, feeddiscovery, datetime):
        self.feed = feed_model
        self.feed_site = feed_site_model
        self.subscription = subscription_model
        self.discovery = feeddiscovery
        self.datetime = datetime

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
        subs =  self.subscription.objects.filter_by_user(user).select_related('feed')
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

class FeedItemService(object):

    @beject.inject
    def __init__(self, feed_item_status_model, datetime):
        self.feed_item_status = feed_item_status_model
        self.datetime = datetime

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


