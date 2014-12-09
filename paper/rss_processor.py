import logging
import itertools

from bs4 import BeautifulSoup
import feedparser
from django.utils.encoding import iri_to_uri

from paucore.utils.data import chunks
from sparksbase.urls import canonicalize_url

from .models import Source, SOURCE_STATUS, SOURCE_KINDS, Article


logger = logging.getLogger(__name__)


def parse_source_into_feed(source):
    if not source.current_version:
        return None

    try:
        return feedparser.parse(source.current_version.content)
    except:
        logger.exception("Failed to parse feed for source_id:%s source_history_id: %s", source.id, source.current_version.id)
        return None


def get_link_for_item(item):
    main_item_link = item.get('link')

    if not main_item_link:
        links = item.get('links', [])
        for link in links:
            href = link.get('href')
            if href:
                main_item_link = href


def prepare_title_from_item(item):
    title_detail = item.get('title_detail')
    title = item.get('title', 'No Title')

    # If the title is HTML then we need to decode it to some kind of usable text
    # Definitely need to decode any entities
    if title_detail:
        if title_detail['type'] == u'text/html':
            title = BeautifulSoup(title).text

    return title


class Entry(dict):

    @classmethod
    def from_feed_entry(cls, feed_entry):

        cls['title'] = prepare_title_from_item(feed_entry)[0:255]
        cls['link'] = iri_to_uri(get_link_for_item(feed_entry))

        if not cls['link']:
            logger.warn("Item found without link skipping feed_entry: %s", feed_entry)
            return

        if len(cls['link']) > 255:
            logger.warn('Found a link > 500 chars link: %s feed_entry: %s', cls['link'], feed_entry)
            return

        cls['_link'] = cls['link']
        cls['link'] = canonicalize_url(cls['_link'])
        cls['summary'] = feed_entry.get('summary', '')
        cls['published'] = feed_entry.get('published')

        if feed_entry.language:
            cls['language'] = feed_entry.language

        if 'tags' in feed_entry:
            cls['tags'] = filter(None, [x['term'] for x in feed_entry.tags])

        if 'author' in feed_entry and feed_entry.author:
            cls['author'] = feed_entry.author

        return cls

    @property
    def title(self):
        return self.get('title')

    @property
    def summary(self):
        return self.get('summary')

    @property
    def link(self):
        self.get('link')


def feeds_to_entries(feeds):
    for feed in feeds:
        for entry in feed.entries:
            yield Entry.from_feed_entry(entry)


def create_article_from(entry):
    articles = Article.objects.filter(url=entry.link)
    if articles.count():
        return articles[0], False

    articles = Article.objects.filter(raw_url=entry.link)
    if articles.count():
        return articles[0], False

    article, created = Article.objects.get_or_create(raw_url=entry.link, processed=False, defaults={
        'title': entry.title,
    })

    return article, created


def process_rss_feeds():
    rss_feeds = Source.objects.filter(status=SOURCE_STATUS.ACTIVE, kind=SOURCE_KINDS.RSS,
                                      needs_update=True)
    total_pass = 0
    total_created = 0
    for chunk in chunks(rss_feeds, 10):
        chunk = chunk.prefetch_related('current_version')
        feeds = itertools.imap(parse_source_into_feed, chunk)
        entries = feeds_to_entries(feeds)
        for entry in entries:
            article, created = create_article_from(entry)

            if created:
                total_created += 1
            else:
                total_pass += 1

    logger.info('Finished processing rss feeds total_pass: %s total_created: %s', total_pass, total_created)
