from celery import shared_task

from .rss_updater import update_rss_feeds
from .rss_processor import process_rss_feeds
from .article_processor import process_articles as proc_articles
from .social_processor import update_facebook_stats


@shared_task()
def update_rss():
    update_rss_feeds()


@shared_task()
def process_rss():
    process_rss_feeds()


@shared_task()
def process_articles():
    proc_articles()


@shared_task()
def update_facebook():
    update_facebook_stats()
