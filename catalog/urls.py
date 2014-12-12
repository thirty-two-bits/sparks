from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^admin/stats/$', 'catalog.views.stats', name='stats'),
    url(r'^articles/$', 'catalog.views.articles', name='articles'),
)
