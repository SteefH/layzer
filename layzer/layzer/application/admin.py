from django.contrib import admin
from layzer.application import models
for model in 'Feed FeedItem Subscription FeedItemStatus FeedSite'.split():
    admin.site.register(getattr(models, model))

