import beject

from layzer.application import models
from layzer.util import feeddiscovery
from layzer.application import SubscriptionService
from datetime import datetime

beject.register({
    'feed_model': models.Feed,
    'subscription_model': models.Subscription,
    'feed_item_status_model': models.FeedItemStatus,
    'feed_site_model': models.FeedSite,
    'feeddiscovery': feeddiscovery,
    'datetime': datetime,
    'SubscriptionService': beject.Singleton(SubscriptionService)
})
