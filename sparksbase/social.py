import logging
import json
import requests

logger = logging.getLogger()


def facebook(urls):
    if isinstance(urls, basestring):
        urls = [urls]

    urls = u','.join(urls)

    params = {
        'urls': urls,
        'format': 'json'
    }

    url = 'https://api.facebook.com/method/links.getStats'

    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
    except:
        logger.exeception("Failed to fetch facebook data for: %s", params)
        return {}

    data = resp.json()

    return {x['url']: x for x in data}


def twitter(url):
    params = {'url': url, 'callback': 'twttr.receiveCount'}
    url = 'http://urls.api.twitter.com/1/urls/count.json'

    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
    except:
        logger.exeception("Failed to fetch twitter data for: %s", params)
        return None

    raw_content = resp.content.replace('twttr.receiveCount(', '')
    raw_content = raw_content.replace(');', '')

    return json.loads(raw_content)
