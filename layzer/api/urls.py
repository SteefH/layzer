from django.conf.urls.defaults import patterns, include
from tastypie.api import Api

from layzer.api.views import SubscriptionResource, FeedItemResource


v1_api = Api(api_name='v1')
v1_api.register(SubscriptionResource())
v1_api.register(FeedItemResource())

urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
)
