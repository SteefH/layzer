import beject

from layzer.application import models
from layzer.util import feeddiscovery
from layzer.application import SubscriptionService, FeedService, FeedItemService
from datetime import datetime
from layzer.util import feedreader

beject.register({
    'feed_model': models.Feed,
    'feed_item_model': models.FeedItem,
    'feed_item_status_model': models.FeedItemStatus,
    'feed_site_model': models.FeedSite,
    'subscription_model': models.Subscription,
    'feeddiscovery': feeddiscovery,
    'datetime': datetime,
    'SubscriptionService': beject.Singleton(SubscriptionService),
    'feed_service': beject.Singleton(FeedService),
    'feed_item_service': beject.Singleton(FeedItemService),
    'feedreader': feedreader
})
