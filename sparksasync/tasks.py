import requests

from celery import shared_task, group


@shared_task()
def urlopen(_id, url):
    print('Opening: {0}'.format(url))
    try:
        response = requests.get(url)
    except Exception as exc:
        print('URL {0} gave error: {1!r}'.format(url, exc))
        return (_id, None)

    return (_id, response)


def crawl_urls(list_of_urls):
    result = group(urlopen.s(_id, url) for _id, url in list_of_urls).apply_async()
    for _id, incoming_result in result.iterate():
        yield _id, incoming_result
