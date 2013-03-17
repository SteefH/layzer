from django.core.exceptions import MiddlewareNotUsed
import beject

class DependencyInjectionMiddleware(object):

    def __init__(self):

        from layzer.application import models
        from layzer.util import feeddiscovery
        from layzer.application import SubscriptionService
        from datetime import datetime
        beject.register({
            'feed_model': models.Feed,
            'subscription_model': models.Subscription,
            'feed_item_status_model': models.FeedItemStatus,
            'feeddiscovery': feeddiscovery,
            'datetime': datetime,
            'SubscriptionService': beject.Singleton(SubscriptionService)
        })
        # to stop further calls to this middleware
        raise MiddlewareNotUsed
