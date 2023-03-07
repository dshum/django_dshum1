from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'message',
        'is_human',
        'created_at',
    )
    search_fields = ('name', 'email', 'message')
    ordering = ('-created_at',)
