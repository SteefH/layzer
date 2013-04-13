"""The models
"""

# pylint: disable=R0903,C0111,W0232,E1101

from django.conf import settings
from django.db import models

Q = models.Q

class FeedManager(models.Manager):

    def find_by_url(self, url):
        query = (
            Q(feed_url=url) |
            Q(site_url=url)
        )
        return self.get(query)

class Feed(models.Model):
    feed_url = models.URLField()
    last_check = models.DateTimeField(null=True)
    last_update = models.DateTimeField(null=True)
    added = models.DateTimeField(auto_now_add=True)

    objects = FeedManager()

    def __unicode__(self):
        return self.feed_url

class FeedSite(models.Model):

    feed = models.ForeignKey(Feed)
    site_url = models.URLField()
    name = models.TextField()

    def __unicode__(self):
        return "{0} ({1})".format(self.name, self.site_url)

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed)
    published_on = models.DateTimeField()
    publisher = models.CharField(max_length=1024, null=True)
    link = models.URLField()
    title = models.CharField(max_length=1024)
    short_body = models.TextField()
    body = models.TextField()

    def __unicode__(self):
        return self.link

    def status_for_user(self, user):
        try:
            return self.statuses.get(user=user)
        except FeedItemStatus.DoesNotExist:
            return None

class SubscriptionManager(models.Manager):

    def get_by_feed_and_user(self, feed, user):
        return self.get(site__feed=feed, user=user)

    def filter_by_user(self, user, include_deleted=False):
        queryset = self.filter(user=user)
        if not include_deleted:
            queryset = queryset.filter(deleted_on=None)
        return queryset

class Subscription(models.Model):
    site = models.ForeignKey(FeedSite)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    added = models.DateTimeField(auto_now_add=True)
    deleted_on = models.DateTimeField(null=True)
    name = models.CharField(max_length=1024, null=True)

    objects = SubscriptionManager()

    def __unicode__(self):
        return u'{!s} -> {}'.format(self.user, self.name)


class FeedItemStatus(models.Model):
    item = models.ForeignKey(FeedItem, related_name='statuses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    kept_unread_on = models.DateTimeField(null=True, default=None)
    starred_on = models.DateTimeField(null=True, default=None)
    read_on = models.DateTimeField(null=True, default=None)

