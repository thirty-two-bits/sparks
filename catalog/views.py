from datetime import datetime, timedelta
import json

from django.http import HttpResponse

from paper.models import Article, Source, Origin


def stats(request):
    data = {}
    articles = Article.objects.all()

    data['total_articles'] = articles.count()
    data['processed_articles'] = articles.filter(processed=True).count()
    data['unprocessed_articles'] = articles.filter(processed=False).count()

    latest_article = articles.order_by('pk').last()
    if latest_article:
        data['latest_article_date'] = unicode(latest_article.created)

    sources = Source.objects.all()
    data['total_sources'] = sources.count()

    origins = Origin.objects.all()
    data['total_origins'] = origins.count()

    return HttpResponse(json.dumps(data), content_type='application/javascript')


def article_to_json(article):
    return {
        'title': article.title,
        'url': article.url,
        'current_facebook_shares': article.current_facebook_shares,
    }


def articles(request):
    data = {}
    three_days_ago = datetime.utcnow() - timedelta(days=3)
    articles = Article.objects.filter(created__gte=three_days_ago, processed=True)[0:200]

    data = map(article_to_json, articles)

    return HttpResponse(json.dumps(data), content_type='application/javascript')
