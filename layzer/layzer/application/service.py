from layzer.application import models
from layzer.util import feeddiscovery

class NoFeedException(Exception):
    """
    Exception raised when there's no feed found at a given url.
    """

class AlreadySubscribedException(Exception):
    """
    Exception raised when the user is already subscribed to a given feed.
    """

def _get_or_create_feed(url):
    try:
        return models.Feed.get_by_url(url)
    except models.Feed.DoesNotExist:
        pass
    try:
        discovery = feeddiscovery.discoverfeed(url)
    except feeddiscovery.FeedException:
        raise NoFeedException
    name, site_url, feed_url = discovery
    feed = models.Feed(name=name, site_url=site_url, feed_url=feed_url)
    feed.save()


def add_subscription(url, user):
    feed = _get_or_create_feed(url)
    try:
        models.Subscription.get_by_feed_and_user(feed, user)
        raise AlreadySubscribedException
    except models.Subscription.DoesNotExist:
        pass
    sub = models.Subscription(feed=feed, user=user, name=feed.name)
    sub.save()
    return sub

