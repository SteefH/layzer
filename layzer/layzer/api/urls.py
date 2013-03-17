from django.conf.urls.defaults import patterns, include
from tastypie.api import Api

from layzer.api.views import SubscriptionResource


v1_api = Api(api_name='v1')
v1_api.register(SubscriptionResource())

urlpatterns = patterns('',
    (r'^', include(v1_api.urls)),
)
