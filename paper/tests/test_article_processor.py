from django.test import TestCase
import responses

from sparksbase.test_utils import create_mock_response

from paper.models import Article
from paper.article_processor import (set_meta_data_for_resp, set_origin_for_article, process_articles)

from .mock_models import MockModel


class TestArticles(MockModel, TestCase):
    def test_set_meta_data_for_resp(self):
        article = self.create_article()
        resp = create_mock_response(self.DEFAULT_ARTICLE_CONTENT)
        article = set_meta_data_for_resp(article, resp)

        self.assertEquals(article.social_data.og.get('site_name'), 'Re/code')
        self.assertEquals(article.article_info.html, self.DEFAULT_ARTICLE_CONTENT)

    def test_set_origin_for_article(self):
        article = self.create_article()

        article = set_origin_for_article(article)

        assert article.origin

        origin1 = article.origin

        article2 = self.create_article(url='http://www.recode.net')

        article2 = set_origin_for_article(article2)

        self.assertEquals(article2.origin.url, origin1.url)

        self.assertEquals(origin1.id, article2.origin.id)

        assert origin1.title == 'recode.net'

    def test_process_articles(self):
        article = self.create_article()
        article.save()
        with responses.mock:
            self.add_article_content_to_responses()
            process_articles()

        article = Article.objects.get(pk=article.pk)

        assert article.processed is True
