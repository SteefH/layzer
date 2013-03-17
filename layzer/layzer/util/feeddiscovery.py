import urlparse
import re

import requests


from bs4 import BeautifulSoup
import feedparser

class FeedException(Exception):
    pass

_link_filter = {
    'rel': re.compile(r'\b(feed|alternate)\b'),
    'type': re.compile(r'\bapplication/(rss|atom)\+xml\b')
}

def _handle_html(r, visited_urls):
    page = BeautifulSoup(r.text)

    links = page.find_all('link',**_link_filter)
    for link in links:
        href = link.get('href')
        if not href:
            continue
        href = urlparse.urljoin(r.url, href)
        result = _discoverfeed(href, visited_urls)
        if result:
            return result
    return None

def _handle_xml(r, visited_urls):
    try:
        result = feedparser.parse(r.content)
    except:
        return None
    return (result.feed.title, result.feed.link, r.url)

def _handle_response(r, visited_urls):
    mime, encoding = (
        r.headers.get('content-type', '').split(';') + ['']
    )[:2]

    if mime == 'text/html':
        return _handle_html(r, visited_urls)
    if mime in ['application/atom+xml', 'application/rss+xml', 'text/xml']:
        return _handle_xml(r, visited_urls)
    # last attempt, strict to lenient
    for f in [_handle_xml, _handle_html]:
        try:
            result = f(r, visited_urls)
            if result:
                return result
        except FeedException:
            raise
        except:
            pass

    raise FeedException('Could not read feed at ' + r.url)

def _discoverfeed(url, visited_urls):
    """Find out the RSS/ATOM feed url for a given url

    returns a tuple of (title, feed_url, website_url), or None
    """
    if not url or url in visited_urls:
        return None

    visited_urls.add(url)
    try:
        r = requests.get(url)
    except:
        raise FeedException('Could not retrieve feed')
    if r.status_code != requests.codes.ok:
        raise FeedException('Could not retrieve feed')
    return _handle_response(r, visited_urls)


def discover(url):
    result = _discoverfeed(url, set())
    if result is None:
        raise FeedException("No feed found")
    return result

if __name__ == '__main__':
    import sys
    print discover(sys.argv[1])
