from datetime import datetime, timedelta
import hashlib
import logging

from .models import Source, SourceHistory, SOURCE_STATUS, SOURCE_KINDS, MAX_FAILURES

from paucore.utils.data import chunks
from sparksasync.tasks import crawl_urls

logger = logging.getLogger(__name__)


def hash_content(text):
    return hashlib.sha256(text).hexdigest()


def set_next_update(model):
    model.next_update = datetime.utcnow() + timedelta(minutes=model.update_freq)
    model.save()

    return model


def update_for_failure(model):
    model.failure_count += 1

    if model.failure_count >= MAX_FAILURES:
        model.status = SOURCE_STATUS.DISABLED_FOR_FAILURE

    model.save()

    return model


def sort_resps(mapped_resps):
    successes = []
    failures = []

    for source, resp in mapped_resps:
        if resp is None:
            failures.append([source, resp])

        elif resp.status_code > 399 or resp.status_code < 200:
            failures.append([source, resp])

        else:
            successes.append([source, resp])

    return successes, failures


def ident(resp):
    etag = resp.headers.get('ETag')
    if not etag:
        etag = hash_content(resp.content)

    return etag


def update_source_history(source, content, etag):
    rev, created = SourceHistory.objects.get_or_create(source=source, etag=etag, defaults={
        'content': content
    })

    if created:
        source.current_version_id = rev.id
        source.needs_update = True

    source.failures_count = 0
    source.status = SOURCE_STATUS.ACTIVE
    source.last_update = datetime.utcnow()
    source.save()

    return rev


def update_sources_for_responses(mapped_resps):
    successes, failures = sort_resps(mapped_resps)

    logger.info('Updated chunk of rss feeds num_success: %s num_failure: %s', len(successes),
                len(failures))

    for source, resp in failures:
        source = update_for_failure(source)

    for source, resp in successes:
        etag = ident(resp)
        update_source_history(source, resp.text, etag)

    return successes, failures


def update_rss_feeds():
    rss_feeds = Source.objects.filter(status=SOURCE_STATUS.ACTIVE, kind=SOURCE_KINDS.RSS,
                                      next_update__lte=datetime.utcnow())
    total_succcess = 0
    total_failures = 0
    total_feeds = 0
    for chunk in chunks(rss_feeds):
        source_by_id = {x.id: x for x in chunk}
        urls = map(lambda x: (x.id, x.url), chunk)

        mapped_resps = []
        for _id, resp in crawl_urls(urls):
            source = source_by_id.get(_id)
            mapped_resps += [(source, resp)]

        successes, failures = update_sources_for_responses(mapped_resps)
        total_succcess += len(successes)
        total_failures += len(failures)
        total_feeds += total_feeds

    logger.info('Finished updating rss feeds total_feeds: %s total_succcess: %s total_failures: %s', total_feeds, total_succcess,
                total_failures)
