import beject

class UpdateFeedsJob(object):

    @beject.inject
    def __init__(self, feedreader, feed_model, feed_item_model):
        self.feedreader = feedreader
        self.feed_model = feed_model
        self.feed_item_mode = feed_item_model

    def read_feeds(self):
        for feed in self.feed_model.objects:
            yield feed, self.read_feed(feed.feed_url)


    def read_feed(self, url):
        return self.feed_reader.read_feed(url)

    def get_feed_items(self, url):
        for feed, read_feed in self.read_feeds():
            for item in read_feed.items:
                yield None

