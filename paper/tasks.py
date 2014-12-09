from celery import shared_task

from .rss_updater import update_rss_feeds


@shared_task()
def update_rss():
    update_rss_feeds()
