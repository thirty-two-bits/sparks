from datetime import datetime, timedelta

from django.http import HttpResponse
from simpleapi import api_handler

from paper.models import Article, Source, Origin
from corsheaders.middleware import CorsMiddleware

cors_middleware = CorsMiddleware()


def allow_cors(func):
    def func_wrapper(request, *args, **kwargs):
        resp = cors_middleware.process_request(request)

        if not resp:
            resp = func(request, *args, **kwargs)

        resp = cors_middleware.process_response(request, resp)

        return resp

    return func_wrapper


@allow_cors
@api_handler
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

    return data


def article_to_json(article):
    return {
        'title': article.title,
        'url': article.url,
        'current_facebook_shares': article.current_facebook_shares,
        'description': article.social_data.description,
        'author': article.article_info.author,
    }


@allow_cors
@api_handler
def articles(request):
    data = {}
    three_days_ago = datetime.utcnow() - timedelta(days=3)
    articles = Article.objects.filter(created__gte=three_days_ago, processed=True)
    articles = articles.order_by('-current_facebook_shares')
    articles = articles[0:200]

    data = map(article_to_json, articles)

    return data


def auth_done(request):
    return HttpResponse('Thanks, we got it from here.')
