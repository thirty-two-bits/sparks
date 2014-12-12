import os
import responses
import vcr

from paper.models import Article, Source, SourceHistory, SOURCE_KINDS


DEFAULT_TEST_FEED_URL = 'http://daringfireball.net/feeds/main'
DEFAULT_ARTICLE_URL = 'http://recode.net/2014/12/04/amazon-unveils-its-own-line-of-diapers-confirming-partners-biggest-fears/'


BASE_DIR = os.path.dirname(__file__) + '/data/'

DEFAULT_RSS_CONTENT = ''
with open(BASE_DIR + 'simple_daringfireball.xml') as fd:
    DEFAULT_RSS_CONTENT = fd.read()


DEFAULT_ARTICLE_CONTENT = ''
with open(BASE_DIR + 'article.html') as fd:
    DEFAULT_ARTICLE_CONTENT = fd.read()

BASE_DIR = os.path.dirname(__file__) + '/data/'
CASSETTE_DIR = BASE_DIR + '/cassettes/'


class MockModel(object):
    DEFAULT_ARTICLE_CONTENT = DEFAULT_ARTICLE_CONTENT
    DEFAULT_RSS_CONTENT = DEFAULT_RSS_CONTENT
    DEFAULT_TEST_FEED_URL = DEFAULT_TEST_FEED_URL
    CASSETTE_DIR = CASSETTE_DIR

    def create_article(self, title='With Rumors Of Another Cellular-Capable Smartwatch, Let\'s Hit The Brakes', url=DEFAULT_ARTICLE_URL):
        return Article.objects.create(title=title, url=url, processed=False)

    def add_article_content_to_responses(self, url=DEFAULT_ARTICLE_URL, body=DEFAULT_ARTICLE_CONTENT):
        responses.add(responses.GET, url,
                      body=body, status=200,
                      content_type='text/html')

    def create_source(self, name='Daring Fireball', url=DEFAULT_TEST_FEED_URL, kind=SOURCE_KINDS.RSS):
        return Source.objects.create(name=name, url=url, kind=kind)

    def create_source_history(self, source, content=DEFAULT_RSS_CONTENT):
        history = SourceHistory.objects.create(source_id=source.id, content=content)

        source.current_version = history
        source.save()

        return history

    def setup_basic_system(self):
        from paper.rss_updater import update_rss_feeds
        from paper.rss_processor import process_rss_feeds
        from paper.article_processor import process_articles

        source = self.create_source()
        source.save()
        with responses.mock:
            responses.add(responses.GET, self.DEFAULT_TEST_FEED_URL,
                          body=self.DEFAULT_RSS_CONTENT, status=200,
                          content_type='application/xml')

            update_rss_feeds()

        with vcr.use_cassette(self.CASSETTE_DIR + '/link_resp.yml'):
            process_rss_feeds()

        with vcr.use_cassette(self.CASSETTE_DIR + '/link_resp.yml'):
            process_articles()
