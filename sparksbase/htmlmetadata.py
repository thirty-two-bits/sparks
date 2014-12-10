from collections import defaultdict
from bs4 import BeautifulSoup


def parse_meta_data(html):
    if not html:
        return None

    if not isinstance(html, BeautifulSoup):
        soup = BeautifulSoup(html)
    else:
        soup = html

    data = defaultdict(dict)
    props = soup.findAll('meta')

    for prop in props:
        key = prop.get('property', prop.get('name'))
        if not key:
            continue

        key = key.split(':')

        value = prop.get('content', prop.get('value'))

        if not value:
            continue

        value = value.strip()

        if value.isdigit():
            value = int(value)

        ref = data[key.pop(0)]

        for idx, part in enumerate(key):
            if not key[idx:-1]:  # no next values
                ref[part] = value
                break
            if not ref.get(part):
                ref[part] = dict()
            else:
                if isinstance(ref.get(part), basestring):
                    ref[part] = {'url': ref[part]}
            ref = ref[part]

    return data
