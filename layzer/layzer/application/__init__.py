
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

    @classmethod
    def create_default(cls):
        """Create the default service
        """
        from layzer.application import models
        from layzer.util import feeddiscovery
        from datetime import datetime
        return cls(models.Feed, models.Subscription, feeddiscovery, datetime)

    @beject.inject
    def __init__(self, feed_model, subscription_model, feeddiscovery, datetime):
        self.feed = feed_model
        self.subscription = subscription_model
        self.discovery = feeddiscovery
        self.datetime = datetime

    def _get_or_create_feed(self, url):
        """
        Get or create a feed model based on a given url. Try to discover
        the feed at the url when there's no feed model yet for the url
        """

        try:
            return self.feed.objects.find_by_url(url)
        except self.feed.DoesNotExist:
            pass
        try:
            name, site_url, feed_url = self.discovery.discover(url)
        except self.discovery.FeedException:
            raise self.NoFeedException
        feed = self.feed(name=name, site_url=site_url, feed_url=feed_url)
        feed.save()
        return feed


    def add_subscription(self, url, user):
        feed = self._get_or_create_feed(url)
        try:
            self.subscription.objects.get_by_feed_and_user(feed, user)
            raise self.AlreadySubscribedException
        except self.subscription.DoesNotExist:
            pass
        sub = self.subscription(feed=feed, user=user, name=feed.name)
        sub.save()
        return sub

    def remove_subscription(self, subscription):
        subscription.deleted_on = self.datetime.now()
        subscription.save()

    def get_all(self, user):
        subs =  self.subscription.objects.filter_by_user(user).select_related('feed')
        return subs


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
