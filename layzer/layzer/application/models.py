"""The models
"""

from django.conf import settings
from django.db import models

Q = models.Q

class Feed(models.Model):
    site_url = models.URLField()
    feed_url = models.URLField()
    name = models.TextField()
    last_check = models.DateTimeField(null=True)
    last_update = models.DateTimeField(null=True)
    added = models.DateTimeField(auto_now_add=True)

    @classmethod
    def find_by_url(cls, url):
        query = (
            Q(feed_url=url) |
            Q(site_url=url)
        )
        return cls.objects.get(query)

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed)
    published_on = models.DateTimeField()
    link = models.URLField()
    title = models.CharField(max_length=1024)
    short_body = models.TextField()
    body = models.TextField()


class Subscription(models.Model):

    feed = models.ForeignKey(Feed)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    added = models.DateTimeField(auto_now_add=True)
    deleted_on = models.DateTimeField(null=True)
    name = models.CharField(max_length=1024, null=True)

    @classmethod
    def get_by_feed_and_user(cls, feed, user):
        return cls.objects.get(feed=feed, user=user)

class FeedItemStatus(models.Model):
    item = models.ForeignKey(FeedItem)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    kept_unread_on = models.DateTimeField(null=True, default=None)
    starred_on = models.DateTimeField(null=True, default=None)
    read_on = models.DateTimeField(null=True, default=None)
