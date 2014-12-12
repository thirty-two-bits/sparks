import vcr

from django.test import TestCase

from paper.models import Source, Article
from paper.rss_processor import (parse_source_into_feed, get_link_for_item, prepare_title_from_item,
                                 Entry, create_article_from, process_rss_feeds)

from .mock_models import MockModel


class TestRssProcessor(MockModel, TestCase):

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
        self.assertEquals(link, "http://recode.net/2014/12/04/amazon-unveils-its-own-line-of-diapers-confirming-partners-biggest-fears/")

    def test_prepare_title_from_item(self):
        source = self.create_source()
        self.create_source_history(source)

        feed = parse_source_into_feed(source)
        title = prepare_title_from_item(feed.entries[0])
        self.assertEquals(title, "Amazon Elements: Amazon Unveils Its Own Diapers and Baby Wipes")

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

    def test_process_rss_feeds(self):
        source = self.create_source()
        self.create_source_history(source)

        with vcr.use_cassette(self.CASSETTE_DIR + '/link_resp.yml'):
            process_rss_feeds()

        source = Source.objects.get(pk=source.id)

        assert source.needs_update is False

        self.assertEquals(Article.objects.count(), 1)
