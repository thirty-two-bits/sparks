from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^admin/stats/$', 'catalog.views.stats', name='stats'),
)
