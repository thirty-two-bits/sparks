import requests
import logging

from celery import shared_task, group

logger = logging.getLogger(__name__)


@shared_task()
def urlopen(_id, url):
    logger.info('Opening: %s', url)
    try:
        response = requests.get(url)
    except Exception:
        logger.exception('URL %s gave error', url)
        return (_id, None)

    return (_id, response)


def crawl_urls(list_of_urls):
    result = group(urlopen.s(_id, url) for _id, url in list_of_urls).apply_async()
    for _id, incoming_result in result.iterate():
        yield _id, incoming_result
