from datetime import datetime, timedelta
import os
import responses

from django.test import TestCase

from sparksbase.test_utils import create_mock_response

from paper.models import Source, DEFAULT_UPDATE_FREQ, SOURCE_STATUS, MAX_FAILURES
from paper.rss_updater import (sort_resps, hash_content, set_next_update, update_for_failure,
                               ident, update_source_history, update_rss_feeds)


from .mock_models import MockModel


BASE_DIR = os.path.dirname(__file__) + '/data/'


class TestSources(MockModel, TestCase):
    def test_sort_resps(self):
        source = self.create_source()
        resp = create_mock_response('')
        resp_bad_http = create_mock_response('', status=404)
        resp_none = None

        resps = [
            (source, resp),
            (source, resp_bad_http),
            (source, resp_none)
        ]

        successes, failures = sort_resps(resps)

        assert len(successes) == 1
        assert len(failures) == 2

    def test_hash_content(self):
        content = '123'
        self.assertEquals('a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', hash_content(content))

    def test_set_next_update(self):
        source = self.create_source()
        five_mins_from_now = datetime.utcnow() + timedelta(minutes=DEFAULT_UPDATE_FREQ)
        six_mins_from_now = datetime.utcnow() + timedelta(minutes=DEFAULT_UPDATE_FREQ + 1)
        source = set_next_update(source)
        assert five_mins_from_now < source.next_update
        assert six_mins_from_now > source.next_update

    def test_update_for_failure(self):
        source = self.create_source()
        source = update_for_failure(source)

        assert source.failure_count == 1
        assert source.status == SOURCE_STATUS.ACTIVE

        for i in xrange(1, MAX_FAILURES):
            source = update_for_failure(source)

        assert source.status == SOURCE_STATUS.DISABLED_FOR_FAILURE

    def test_ident(self):
        resp_no_etag = create_mock_response(self.DEFAULT_RSS_CONTENT)
        etag = 'xyz'
        resp_etag = create_mock_response(self.DEFAULT_RSS_CONTENT, extra_headers={
            'ETag': etag
        })

        self.assertEquals(etag, ident(resp_etag))
        self.assertEquals('5f5424e1ce213e5803299db41c3245f2018c80087a7e4b11abe2e0d230d59f46', ident(resp_no_etag))

    def test_update_source_history(self):
        source = self.create_source()
        resp = create_mock_response('')
        etag = ident(resp)
        rev_1 = update_source_history(source, resp.text, etag)
        resp = create_mock_response(self.DEFAULT_RSS_CONTENT)
        etag = ident(resp)
        rev_2 = update_source_history(source, resp.text, etag)

        assert rev_1.id != rev_2.id

        resp = create_mock_response(self.DEFAULT_RSS_CONTENT)
        etag = ident(resp)
        rev_3 = update_source_history(source, resp.text, etag)

        assert rev_2.id == rev_3.id

        resp = create_mock_response(self.DEFAULT_RSS_CONTENT, extra_headers={
            'ETag': '123',
        })

        # Pretend that and update has happend
        source.needs_update = False
        source.save()

        etag = ident(resp)
        rev_4 = update_source_history(source, resp.text, etag)
        assert rev_3.id != rev_4.id

        source = Source.objects.get(id=source.id)

        assert source.needs_update is True

    def test_update_rss_feeds(self):
        source = self.create_source()
        source.save()
        with responses.mock:
            responses.add(responses.GET, self.DEFAULT_TEST_FEED_URL,
                          body=self.DEFAULT_RSS_CONTENT, status=200,
                          content_type='application/xml')

            update_rss_feeds()

        source = Source.objects.get(id=source.id)

        assert source.current_version is not None
