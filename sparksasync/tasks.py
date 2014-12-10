import requests
from requests.exceptions import ConnectionError
import logging

from celery import shared_task, group

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def urlopen(self, _id, url, timeout=30, headers=None):
    logger.info('Opening: %s', url)

    headers = {
        'User-Agent': 'Pangea Meta Data Bot v.1',
    }

    if headers:
        headers.update(headers)

    try:
        response = requests.get(url, headers=headers)
    except ConnectionError, e:
        raise self.retry(exc=e)
    except Exception:
        logger.exception('URL %s gave error', url)
        return (_id, None)

    return (_id, response)


def crawl_urls(list_of_urls, timeout=30):
    result = group(urlopen.s(_id, url, timeout=timeout) for _id, url in list_of_urls).apply_async()
    for _id, incoming_result in result.iterate():
        yield _id, incoming_result
