import logging

from paucore.utils.data import qs_iter_chunks
from sparksasync.tasks import crawl_urls
from sparksbase.htmlmetadata import parse_meta_data

from .models import Article, Origin

logger = logging.getLogger(__name__)


def set_meta_data_for_resp(article, resp):
    meta_data = parse_meta_data(resp.content)

    article.article_info.html = resp.content

    if 'og' in meta_data:
        article.social_data.og = meta_data['og']

    if 'twitter' in meta_data:
        article.social_data.twitter = meta_data['twitter']

    return article


def set_origin_for_article(article):
    if not article.origin:
        origin, created = Origin.objects.get_or_create(url=article.domain, defaults={
            'title': article.domain
        })

        article.origin = origin

    return article


def process_articles():
    for articles in qs_iter_chunks(Article.objects.filter(processed=False), n=10):
        links = ((_id, x.url) for _id, x in articles.items() if x.url)

        for _id, resp in crawl_urls(links):
            article = articles.get(_id)
            if not resp:
                logger.error("Failed to fetch page for article_id: %s url: %s", article.id, article.url)
                continue

            if resp.status_code < 200 and resp.status_code > 299:
                logger.error("Failed to fetch page for article_id: %s url: %s response_code: %s",
                             article.id, article.url, resp.status_code)
                continue

            article = set_meta_data_for_resp(article, resp)
            article = set_origin_for_article(article)

            article.processed = True
            article.save()

            logger.info('Processed article_id: %s article_url: %s', article.id, article.url)
