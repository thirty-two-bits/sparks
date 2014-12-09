from django.contrib import admin
from .models import SourceHistory, Source, Origin, Article


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', )


admin.site.register(Source, SourceAdmin)
admin.site.register(SourceHistory)
admin.site.register(Origin)
admin.site.register(Article)
