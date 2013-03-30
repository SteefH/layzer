
from django.conf.urls import url

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


class SubscriptionObject(object):
    pass


@beject.inject(
    subscription_service='SubscriptionService'
)
class SubscriptionResource(Resource):

    site_url = fields.CharField(blank=False, readonly=True)
    name = fields.CharField(null=True)

    class Meta(object):
        object_class = SubscriptionObject
        # authentication = SessionAuthentication()
        authentication = Authentication()
        authorization = Autho()
        always_return_data = True
        include_resource_uri = True
        detail_uri_name = 'pk'

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/(?P<%s>.+)$" % (
                    self._meta.resource_name,
                    self._meta.detail_uri_name,
                    #trailing_slash()
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
        try:
            bundle.obj = self.subscription_service.add_subscription(
                bundle.data.get('site_url'), bundle.request.user
            )
        except self.subscription_service.AlreadySubscribedException:
            self.raise_error(bundle, 'Already subscribed', http.HttpConflict)
        return bundle

    def obj_update(self, bundle, **kwargs):
        try:
            bundle.obj = self.subscription_service.save_subscription(
                kwargs['pk'], bundle.data, bundle.request.user
            )
        except self.subscription_service.DoesNotExistException:
            self.raise_error(bundle, 'Not found', http.HttpNotFound)
        return bundle

    def obj_delete(self, bundle, **kwargs):
        self.subscription_service.delete_subscription(
            kwargs['pk'], bundle.request.user
        )
        bundle.obj = None
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

@beject.inject(
    'feed_item_service'
)
class FeedItemResource(Resource):

    item_url = fields.CharField(blank=False, readonly=True)
    title = fields.CharField(readonly=True, null=True)
    published_on = fields.DateTimeField(readonly=True)
    body = fields.CharField(readonly=True)
    feed = fields.CharField(readonly=True, null=True)
    marked_read_on = fields.DateTimeField(null=True, readonly=True)
    marked_read = fields.BooleanField()


    class Meta(object):
        object_class = SubscriptionObject
        # authentication = SessionAuthentication()
        authentication = Authentication()
        authorization = Autho()
        always_return_data = True
        include_resource_uri = True
        detail_uri_name = 'pk'
        filtering = {
            "feed": ('exact',),
        }


    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/(?P<%s>.+)$" % (
                    self._meta.resource_name,
                    self._meta.detail_uri_name,
                    #trailing_slash()
                ),
                self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"
            ),
        ]

    def dehydrate(self, bundle, for_list=False):
        feed_item = bundle.obj

        status = feed_item.status_for_user(bundle.request.user)
        read_on = status and status.read_on

        bundle.data.update({
            'id': feed_item.link,
            'item_url': feed_item.link,
            'feed': feed_item.feed.feed_url,
            'published_on': feed_item.published_on,
            'marked_read_on': read_on,
            'marked_read': read_on is not None,
            'title': feed_item.title
        })
        return bundle

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        return super(FeedItemResource, self).build_filters(filters)

    def obj_get_list(self, bundle, **kwargs):
        filters = {}

        if hasattr(bundle.request, 'GET'):
            # Grab a mutable copy.
            filters = bundle.request.GET.copy()

        # Update with the provided kwargs.
        filters.update(kwargs)
        applicable_filters = self.build_filters(filters=filters)
        filters = {}
        if 'feed' in applicable_filters:
            filters['feed__feed_url'] = applicable_filters['feed']
        return self.feed_item_service.get_all(**filters)
