from django.urls import path
from . import views

urlpatterns = [
    path(
        'notifications/',
        views.NotificationViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='notification-list'
    ),
    path(
        'notifications/<int:pk>/',
        views.NotificationViewSet.as_view({
            'get': 'retrieve',
            'delete': 'destroy' 
        }),
        name='notification-detail'
    ),
    path(
        'notifications/<int:pk>/mark_as_read/',
        views.NotificationViewSet.as_view({'post': 'mark_as_read'}),
        name='notification-mark-read'
    ),
    path(
        'notifications/mark_all_read/',
        views.NotificationViewSet.as_view({'post': 'mark_all_read'}),
        name='notification-mark-all-read'
    ),
    path(
        'notifications/unread_count/',
        views.NotificationViewSet.as_view({'get': 'unread_count'}),
        name='notification-unread-count'
    ),
    path(
        'notifications/recent_notifications/',
        views.NotificationViewSet.as_view({'get': 'recent_notifications'}),
        name='notification-recent'
    ),
    path(
        'notifications/summary/',
        views.NotificationViewSet.as_view({'get': 'notification_summary'}),
        name='notification-summary'
    ),
    path(
        'notifications/send/',
        views.NotificationViewSet.as_view({'post': 'send_notification'}),
        name='notification-send'
    ),
    path(
        'notifications/broadcast/', 
        views.NotificationViewSet.as_view({'post': 'broadcast_notification'}),
        name='notification-broadcast'
    ),
    path(
        'notifications/<int:pk>/delete/',
        views.NotificationViewSet.as_view({'delete': 'delete_notification'}),
        name='notification-delete'
    ),
    path(
        'notification-templates/',
        views.NotificationTemplateViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='notificationtemplate-list'
    ),
    path(
        'notification-templates/<int:pk>/',
        views.NotificationTemplateViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='notificationtemplate-detail'
    ),
    path(
        'notification-templates/<int:pk>/toggle_status/',
        views.NotificationTemplateViewSet.as_view({'post': 'toggle_status'}),
        name='notificationtemplate-toggle-status'
    ),
    path(
        'notification-templates/<int:pk>/preview/',
        views.NotificationTemplateViewSet.as_view({'post': 'preview_template'}),
        name='notificationtemplate-preview'
    ),
    path(
        'notification-templates/create_from_template/',
        views.NotificationTemplateViewSet.as_view({'post': 'create_from_template'}),
        name='notificationtemplate-create-from-template'
    ),
]