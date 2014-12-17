from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('accounts/profile/', 'catalog.views.auth_done'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('catalog.urls')),
)
