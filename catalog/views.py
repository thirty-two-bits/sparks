from datetime import datetime, timedelta

from corsheaders.middleware import CorsMiddleware
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage
from simpleapi import api_handler

from paucore.utils.python import cast_int
from paper.models import Article, Source, Origin


cors_middleware = CorsMiddleware()

DEFAULT_NUM_OBJECTS = 200


def paginate_queryset(request, queryset):
    per_page = cast_int(request.GET.get('per_page'), DEFAULT_NUM_OBJECTS)
    meta_content = request.META.get('_meta_content') or {}

    paginator = Paginator(queryset, per_page)

    page = cast_int(request.GET.get('page'), 1)

    if page < 1:
        page = 1

    try:
        section = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        section = paginator.page(paginator.num_pages)

    data = {
        'more': section.has_next(),
        'total': paginator.count,
        'total_pages': paginator.num_pages,
        'page': page,
    }

    if section.has_next():
        data['next_page'] = section.next_page_number()

    if section.has_previous():
        data['prev_page'] = section.previous_page_number()

    meta_content.update(data)

    request.META['_meta_content'] = meta_content

    return section.object_list


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
        'title': article.effective_title,
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
    articles = paginate_queryset(request, articles)

    data = map(article_to_json, articles)

    return data


def auth_done(request):
    return HttpResponse('Thanks, we got it from here.')
