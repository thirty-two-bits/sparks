import json

from django.test import TestCase

from paper.tests.mock_models import MockModel


class TestApi(MockModel, TestCase):
    def test_admin_stats_endpoint(self):
        """
        {
            total_sources: 0,
            total_articles: 0,
            total_origins: 0,
            processed_articles: 0,
            unprocessed_articles: 0
        }
        """
        self.setup_basic_system()
        response = self.client.get('/api/admin/stats/')
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content)
        print resp
        self.assertEquals(resp['total_sources'], 1)
        self.assertEquals(resp['total_articles'], 1)
        self.assertEquals(resp['processed_articles'], 1)
        self.assertEquals(resp['unprocessed_articles'], 0)

        assert 'latest_article_date' in resp
        assert resp['latest_article_date'] != ''

        self.assertEquals(resp['total_origins'], 1)
