from django.contrib import admin

from .models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        'full_url',
        'short_url',
        'requests_count',
        'created_at',
        'is_active',
    )
    search_fields = ('full_url', 'short_url')
    ordering = ('-created_at',)
