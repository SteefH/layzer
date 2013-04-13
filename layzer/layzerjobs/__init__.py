import beject
import datetime
from enumerable import enumerable
from django.utils.timezone import utc

import time


@beject.inject(
    'feed_service',
    'feed_item_service',
    'feedreader',
    transformer='feed_content_transformer'
)
class UpdateFeedsJob(object):

    def read_feed(self, feed):
        return feed, self.feedreader.read_feed(feed.feed_url)

    def get_feed_items(self, args):
        feed, parsed_feed = args
        for item in parsed_feed.entries:
            yield feed, item

    def transform_content(self, content):
        return self.transformer.transform(content)

    def update_item(self, args):
        feed, item = args
        t = time.mktime(item.published_parsed)

        summary = item.get('summary', '')
        content = item.get('content', '')
        if content:
            content = content[0].value
        else:
            content = summary

        content = self.transform_content(content)
        author = item.get('author', '')
        self.feed_item_service.add_or_update_item(
            feed,
            url=item['link'],
            title=item['title'],
            content=content,
            excerpt=summary,
            published_on=datetime.datetime.utcfromtimestamp(t).replace(tzinfo=utc),
            author=author,
            author_link=None,
            author_email=None
        )
        print feed.feed_url, item.link

    def run(self):
        (
            enumerable(self.feed_service.get_all())
                .select(self.read_feed)
                .selectmany(self.get_feed_items)
                .forEach(self.update_item)
        ).execute()
