
from tastypie import fields
from tastypie.resources import Resource
from tastypie.authentication import SessionAuthentication

#from layzer.application import SubscriptionService
import beject

class SubscriptionObject(object):
    pass


class SubscriptionResource(Resource):

    feed_url = fields.CharField(readonly=True)
    site_url = fields.CharField()
    name = fields.CharField()

    class Meta(object):
        object_class = SubscriptionObject
        authentication = SessionAuthentication()

    _subscription_service = None
    @property
    def subscription_service(self):
        if self._subscription_service is None:
            self._subscription_service = beject.get('SubscriptionService')
        return self._subscription_service

    def obj_get_list(self, bundle, **kwargs):
        return self.subscription_service.get_all(bundle.request.user)

    def full_dehydrate(self, bundle, for_list=False):
        bundle.data.update({
            'feed_url': bundle.obj.feed.feed_url,
            'site_url': bundle.obj.feed.site_url,
            'name': bundle.obj.name or bundle.obj.feed.name
        })
        return bundle

