import os

from django.test import TestCase

from paper.models import Source, SourceHistory, Article, SOURCE_KINDS
from paper.rss_processor import (parse_source_into_feed, get_link_for_item, prepare_title_from_item,
                                 Entry, create_article_from, process_rss_feeds)

DEFAULT_TEST_FEED_URL = 'http://daringfireball.net/feeds/main'
BASE_DIR = os.path.dirname(__file__) + '/data/'

DEFAULT_RSS_CONTENT = ''
with open(BASE_DIR + 'daringfireball_2014_12_08.xml') as fd:
    DEFAULT_RSS_CONTENT = fd.read()


class TestSources(TestCase):
    def create_source(self, name='Daring Fireball', url=DEFAULT_TEST_FEED_URL, kind=SOURCE_KINDS.RSS):
        return Source.objects.create(name=name, url=url, kind=kind)

    def create_source_history(self, source, content=DEFAULT_RSS_CONTENT):
        history = SourceHistory.objects.create(source_id=source.id, content=content)

        source.current_version = history
        source.save()

        return history

    def test_parse_source_into_feed(self):
        source = self.create_source()
        self.create_source_history(source)

        feed = parse_source_into_feed(source)
        self.assertEquals(feed.feed.title, 'Daring Fireball')

    def test_get_link_for_item(self):
        source = self.create_source()
        self.create_source_history(source)

        feed = parse_source_into_feed(source)
        link = get_link_for_item(feed.entries[0])
        self.assertEquals(link, "http://www.paddedspaces.com/?df")

    def test_prepare_title_from_item(self):
        source = self.create_source()
        self.create_source_history(source)

        feed = parse_source_into_feed(source)
        title = prepare_title_from_item(feed.entries[0])
        self.assertEquals(title, "Padded Spaces")

    def test_create_article_from(self):
        source = self.create_source()
        self.create_source_history(source)

        feed = parse_source_into_feed(source)
        entry = Entry.from_feed_entry(feed.entries[0])
        article1, created = create_article_from(entry)

        assert created is True
        assert article1.processed is False

        article2, created = create_article_from(entry)

        assert article1.id == article2.id
        assert created is False
        assert article2.url is None

    def test_process_rss_feeds(self):
        source = self.create_source()
        self.create_source_history(source)
        process_rss_feeds()
        source = Source.objects.get(pk=source.id)

        assert source.needs_update is False

        assert Article.objects.count() == 46
