from django.contrib import admin
from .models import SourceHistory, Source, Origin, Article


admin.site.register(Source)
admin.site.register(SourceHistory)
admin.site.register(Origin)
admin.site.register(Article)
