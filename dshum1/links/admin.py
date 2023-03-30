from django.contrib import admin

from .models import Link, LinkTag


@admin.register(LinkTag)
class LinkTagAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'url',
        'user',
        'created_at',
    )
    search_fields = ('title', 'url', 'user')
    ordering = ('-id',)
