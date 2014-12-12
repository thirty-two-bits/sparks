from datetime import datetime, timedelta

from paucore.utils.data import qs_iter_chunks
from sparksbase.social import facebook

from .models import Article


def update_facebook_stats():
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    articles = Article.objects.filter(processed=True, created__gte=seven_days_ago)
    for chunk in qs_iter_chunks(articles, n=100):
        urls = {x.url: x for x in chunk.values()}

        results = facebook(urls.keys())
        for url, result in results.iteritems():
            article = urls.get(url)
            if article:
                article.current_facebook_shares = result.get('share_count', 0)
                article.save()
