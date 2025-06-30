from django.contrib import admin
from .models import Notification, NotificationTemplate

# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'recipient', 'sender', 'notification_type',
        'priority', 'is_read', 'is_sent', 'send_email', 'send_sms', 'send_push',
        'created_at', 'read_at'
    )
    list_filter = (
        'notification_type', 'priority', 'is_read', 'is_sent',
        'send_email', 'send_sms', 'send_push', 'created_at'
    )
    search_fields = (
        'title', 'message', 'recipient__username', 'sender__username',
        'related_object_type', 'related_object_id'
    )
    autocomplete_fields = ['recipient', 'sender']
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'notification_type', 'subject_template', 'is_active'
    )
    list_filter = ('notification_type', 'is_active')
    search_fields = ('name', 'notification_type', 'subject_template')
    ordering = ('name',)