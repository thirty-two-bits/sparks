from datetime import datetime
import json
from urlparse import urlparse

from django.db import models

from paucore.data.fields import CreateDateTimeField, LastModifiedDateTimeField, DictField, Choices
from paucore.utils.date import datetime_to_secs


ORIGIN_KINDS = Choices(
    (1, 'CURATED', 'curated'),
    (2, 'RSS_FEED', 'rss feed'),
)

DEFAULT_UPDATE_FREQ = 5


class Origin(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True, unique=True)
    created = CreateDateTimeField()
    updated = LastModifiedDateTimeField()
    source = models.IntegerField(blank=True, null=True)
    kind = models.IntegerField(blank=True, null=True, choices=ORIGIN_KINDS, default=ORIGIN_KINDS.CURATED)
    extra = DictField(default=dict)


class SocialDatum(dict):
    def normalise(self, output):
        if not output:
            return ''

        return output

    def __repr__(self):
        return self.normalise(self.get('og', self.get('twitter', '')))

    def __unicode__(self):
        return self.normalise(self.get('og', self.get('twitter', '')))

    @property
    def twitter(self):
        return self.normalise(self.get('twitter', ''))

    @property
    def og(self):
        return self.normalise(self.get('og', ''))


class Article(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True, unique=True)
    raw_url = models.CharField(max_length=255, null=True, blank=True, unique=True)
    processed = models.BooleanField(default=False)
    created = CreateDateTimeField()
    updated = LastModifiedDateTimeField()
    origin = models.IntegerField(blank=True, null=True)
    extra = DictField(default=dict)
    init_twitter_shares = models.IntegerField(blank=True, null=True)
    init_facebook_shares = models.IntegerField(blank=True, null=True)
    init_pinterest_shares = models.IntegerField(blank=True, null=True)
    init_total_shares = models.IntegerField(blank=True, null=True)
    current_twitter_shares = models.IntegerField(blank=True, null=True)
    current_facebook_shares = models.IntegerField(blank=True, null=True)
    current_pinterest_shares = models.IntegerField(blank=True, null=True)
    current_total_shares = models.IntegerField(blank=True, null=True)

    def update_timeseries(self):
        timeseries = self.extra.get('timeseries', [])
        timeseries.append([datetime_to_secs(datetime.utcnow()), self.current_total_shares])
        self.extra['timeseries'] = timeseries

    def simple_time_series(self, cap=480):
        timeseries = self.extra.get('timeseries', [])
        if not timeseries:
            return [0] * cap

        timeseries = [x[1] for x in timeseries]
        timeseries = timeseries[-cap:]
        timeseries = ([timeseries[0]] * (cap - len(timeseries))) + timeseries
        return json.dumps(timeseries)

    def __repr__(self):
        return '<SiteArticle %r %r>' % (self.get_site_display(), self.title)

    def social_data(self, key):
        data = SocialDatum()
        if not self.extra:
            return data

        meta_data = self.extra.get('meta_data')
        if not meta_data:
            return data

        if 'og' in meta_data:
            data['og'] = meta_data['og'].get(key)

        if 'twitter' in meta_data:
            data['twitter'] = meta_data['twitter'].get(key)

        return data

    @property
    def social_description(self):
        return self.social_data('description')

    @property
    def social_title(self):
        return self.social_data('title')

    @property
    def social_image(self):
        image = self.extra.get('meta_data', {}).get('og', {}).get('image')

        if isinstance(image, basestring):
            return image

        if isinstance(image, dict):
            return image.get('src', '')

        return None

    @property
    def domain(self):
        parts = urlparse(self.url)
        netloc = parts.netloc
        return netloc.replace('www.', '')


class SourceHistory(models.Model):
    source = models.ForeignKey("Source", blank=True, null=True)
    created = CreateDateTimeField()
    updated = LastModifiedDateTimeField()
    extra = DictField(default=dict)
    etag = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)

SOURCE_KINDS = Choices(
    (1, 'RSS', 'rss'),
    (2, 'BUZZ_SUMO', 'buzz sumo'),
)

SOURCE_STATUS = Choices(
    (10, 'ACTIVE', 'Active'),
    (20, 'DISABLED', 'Disabled'),
    (30, 'DISABLED_FOR_FAILURE', 'Disabled for failures'),
)

MAX_FAILURES = 10


class Source(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, null=True, blank=True, unique=True)
    kind = models.IntegerField(blank=True, null=True, choices=ORIGIN_KINDS, default=ORIGIN_KINDS.CURATED)
    update_freq = models.IntegerField(blank=True, null=True, default=DEFAULT_UPDATE_FREQ)
    failure_count = models.IntegerField(blank=True, null=True, default=0)
    status = models.IntegerField(blank=True, null=True, default=SOURCE_STATUS.ACTIVE, choices=SOURCE_STATUS)
    last_update = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    next_update = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    needs_update = models.BooleanField(default=True)
    etag = models.CharField(max_length=255, blank=True, null=True)
    current_version = models.ForeignKey(SourceHistory, blank=True, null=True, related_name='canonical_source')
    created = CreateDateTimeField()
    updated = LastModifiedDateTimeField()
    extra = DictField(default=dict)
