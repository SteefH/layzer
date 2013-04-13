import feedparser

def read_feed(feed_url):
    return feedparser.parse(feed_url)
