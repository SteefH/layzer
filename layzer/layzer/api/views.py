
from django.conf.urls.defaults import url

from tastypie import http
from tastypie import fields
from tastypie.resources import Resource
from tastypie.bundle import Bundle
from tastypie.authentication import SessionAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.utils import trailing_slash
from tastypie.exceptions import ImmediateHttpResponse
#from layzer.application import SubscriptionService
import beject
import urllib

class Autho(Authorization):

    def create_list(self, *args, **kwds):
        result = super(Autho, self).create_list(*args, **kwds)
        return result

from lazyproperty import lazyproperty

class SubscriptionObject(object):
    pass


class SubscriptionResource(Resource):

    site_url = fields.CharField(blank=False)
    name = fields.CharField(null=True)

    class Meta(object):
        object_class = SubscriptionObject
        # authentication = SessionAuthentication()
        authentication = Authentication()
        authorization = Autho()
        always_return_data = True
        include_resource_uri = True
        detail_uri_name = 'pk'

    _subscription_service = None


    @lazyproperty
    @beject.inject
    def subscription_service(self, SubscriptionService):
        return SubscriptionService

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/(?P<%s>[^/]+)%s$" % (
                    self._meta.resource_name,
                    self._meta.detail_uri_name,
                    trailing_slash()
                ),
                self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"
            ),
        ]

    def raise_error(self, bundle, error, response_class):
        raise ImmediateHttpResponse(
            self.error_response(bundle.request, {'error': error}, response_class)
        )

    def detail_uri_kwargs(self, bundle_or_obj):
        if isinstance(bundle_or_obj, Bundle):
            obj = bundle_or_obj.obj
        else:
            obj = bundle_or_obj

        return {'pk': urllib.quote(obj.site.feed.feed_url, '') }

    def obj_get_list(self, bundle, **kwargs):
        return self.subscription_service.get_all(bundle.request.user)

    def obj_create(self, bundle, **kwargs):
        site_url = bundle.data.get('site_url')
        try:
            bundle.obj = self.subscription_service.add_subscription(
                bundle.data.get('site_url'), bundle.request.user
            )
        except self.subscription_service.AlreadySubscribedException:
            self.raise_error(bundle, 'Already subscribed', http.HttpConflict)
        return bundle

    def dehydrate(self, bundle, for_list=False):
        site = bundle.obj.site
        feed = site.feed
        bundle.data.update({
            'id': feed.feed_url,
            'site_url': site.site_url,
            'name': bundle.obj.name or feed.name
        })
        return bundle

