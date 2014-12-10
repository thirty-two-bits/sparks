from django.contrib import admin
from .models import SourceHistory, Source, Origin, Article


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', )


class OriginAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', )


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', )


admin.site.register(Source, SourceAdmin)
admin.site.register(SourceHistory)
admin.site.register(Origin, OriginAdmin)
admin.site.register(Article, ArticleAdmin)
