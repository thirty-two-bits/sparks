import os

from django.test import TestCase
import responses

from sparksbase.test_utils import create_mock_response

from paper.models import Article
from paper.article_processor import (set_meta_data_for_resp, set_origin_for_article, process_articles)

DEFAULT_ARTICLE_URL = 'http://techcrunch.com/2014/12/09/with-rumors-of-another-cellular-capable-smartwatch-lets-hit-the-breaks/'
BASE_DIR = os.path.dirname(__file__) + '/data/'

DEFAULT_ARTICLE_CONTENT = ''
with open(BASE_DIR + 'article.html') as fd:
    DEFAULT_ARTICLE_CONTENT = fd.read()


class TestArticles(TestCase):
    def create_article(self, title='With Rumors Of Another Cellular-Capable Smartwatch, Let\'s Hit The Brakes', url=DEFAULT_ARTICLE_URL):
        return Article.objects.create(title=title, url=url, processed=False)

    def test_set_meta_data_for_resp(self):
        article = self.create_article()
        resp = create_mock_response(DEFAULT_ARTICLE_CONTENT)
        article = set_meta_data_for_resp(article, resp)

        self.assertEquals(article.social_data.og.get('site_name'), 'TechCrunch')
        self.assertEquals(article.article_info.html, DEFAULT_ARTICLE_CONTENT)

    def test_set_origin_for_article(self):
        article = self.create_article()

        article = set_origin_for_article(article)

        assert article.origin

        origin1 = article.origin

        article2 = self.create_article(url='http://www.techcrunch.com/')

        article2 = set_origin_for_article(article2)

        self.assertEquals(article2.origin.url, origin1.url)

        self.assertEquals(origin1.id, article2.origin.id)

        assert origin1.title == 'techcrunch.com'

    def test_process_articles(self):
        article = self.create_article()
        article.save()
        with responses.mock:
            responses.add(responses.GET, DEFAULT_ARTICLE_URL,
                          body=DEFAULT_ARTICLE_CONTENT, status=200,
                          content_type='text/html')
            process_articles()

        article = Article.objects.get(pk=article.pk)

        assert article.processed is True
