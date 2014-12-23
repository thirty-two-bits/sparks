import json

from django.test import TestCase

from paper.tests.mock_models import MockModel


class TestApi(MockModel, TestCase):
    def setUp(self):
        self.setup_basic_system()

    def test_cors(self):
        response = self.client.options('/api/admin/stats', HTTP_ORIGIN='http://localhost:9000', HTTP_ACCESS_CONTROL_REQUEST_METHOD='GET')
        assert response.status_code == 200
        assert response['Access-Control-Allow-Origin'] == 'http://localhost:9000'
        response = self.client.get('/api/admin/stats', HTTP_ORIGIN='http://localhost:9000')
        assert response['Access-Control-Allow-Origin'] == 'http://localhost:9000'

    def test_admin_stats_endpoint(self):
        response = self.client.get('/api/admin/stats')
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content)
        self.assertEquals(resp['data']['total_sources'], 1)
        self.assertEquals(resp['data']['total_articles'], 1)
        self.assertEquals(resp['data']['processed_articles'], 1)
        self.assertEquals(resp['data']['unprocessed_articles'], 0)

        assert 'latest_article_date' in resp['data']
        assert resp['data']['latest_article_date'] != ''

        self.assertEquals(resp['data']['total_origins'], 1)

    def test_article_view(self):
        response = self.client.get('/api/articles')
        self.assertEqual(response.status_code, 200)
        resp = json.loads(response.content)
        assert len(resp['data']) == 1

        assert 'title' in resp['data'][0]
        assert resp['data'][0]['title'] != ''
