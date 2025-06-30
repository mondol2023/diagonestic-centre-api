from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Notification, NotificationTemplate
from .serializers import NotificationSerializer, NotificationTemplateSerializer
from accounts.models import User

# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'priority', 'is_read', 'is_sent']
    search_fields = ['title', 'message']
    ordering_fields = ['created_at', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'ADMIN':
            return Notification.objects.all()
        else:
            return Notification.objects.filter(recipient=user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = get_object_or_404(Notification, pk=pk)
        if notification.recipient != request.user and request.user.user_type != 'ADMIN':
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()
        
        return Response({'message': 'Notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        notifications = self.get_queryset().filter(is_read=False)
        
        count = notifications.update(
            is_read=True,
            read_at=timezone.now()
        )
        return Response({
            'message': f'{count} marked as read'
        })
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})
    
    @action(detail=False, methods=['get'])
    def recent_notifications(self, request):
        seven_days_ago = timezone.now() - timezone.timedelta(days=7)
        recent = self.get_queryset().filter(
            created_at__gte=seven_days_ago
        ).order_by('-created_at')[:20]
        
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def notification_summary(self, request):
        queryset = self.get_queryset()
        
        type_summary = {}
        for notif_type, display_name in Notification.NOTIFICATION_TYPES:
            type_count = queryset.filter(notification_type=notif_type).count()
            unread_count = queryset.filter(
                notification_type=notif_type, 
                is_read=False
            ).count()
            type_summary[notif_type] = {
                'total': type_count,
                'unread': unread_count,
                'display_name': display_name
            }
        priority_summary = {}
        for priority, display_name in Notification.PRIORITY_LEVELS:
            priority_count = queryset.filter(priority=priority).count()
            unread_count = queryset.filter(
                priority=priority, 
                is_read=False
            ).count()
            priority_summary[priority] = {
                'total': priority_count,
                'unread': unread_count,
                'display_name': display_name
            }
        
        return Response({
            'by_type': type_summary,
            'by_priority': priority_summary,
            'total_notifications': queryset.count(),
            'total_unread': queryset.filter(is_read=False).count()
        })
    
    @action(detail=False, methods=['post'])
    def send_notification(self, request):
        if request.user.user_type not in ['ADMIN', 'RECEPTIONIST', 'DOCTOR']:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        data = request.data.copy()
        data['sender'] = request.user.id
        
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            notification = serializer.save()
            self._send_notification_async(notification)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def broadcast_notification(self, request):
        """Send notification to multiple users"""
        if request.user.user_type not in ['ADMIN']:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        recipient_ids = request.data.get('recipient_ids', [])
        user_types = request.data.get('user_types', [])
        recipients = User.objects.filter(is_active=True)
        
        if recipient_ids:
            recipients = recipients.filter(id__in=recipient_ids)
        elif user_types:
            recipients = recipients.filter(user_type__in=user_types)
        else:
            return Response(
                {'error': 'Either recipient_ids or user_types must be provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        notifications_created = []
        for recipient in recipients:
            notification_data = {
                'recipient': recipient,
                'sender': request.user,
                'notification_type': request.data.get('notification_type', 'SYSTEM'),
                'priority': request.data.get('priority', 'MEDIUM'),
                'title': request.data.get('title', ''),
                'message': request.data.get('message', ''),
                'send_email': request.data.get('send_email', False),
                'send_sms': request.data.get('send_sms', False),
                'send_push': request.data.get('send_push', True),
            }
            notification = Notification.objects.create(**notification_data)
            notifications_created.append(notification)
            self._send_notification_async(notification)
        
        return Response({
            'message': f'{len(notifications_created)} notifications sent',
            'recipients_count': len(notifications_created)
        })
    
    @action(detail=True, methods=['delete'])
    def delete_notification(self, request, pk=None):
        notification = get_object_or_404(Notification, pk=pk)
        if notification.recipient != request.user and request.user.user_type != 'ADMIN':
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        notification.delete()
        return Response({'message': 'Notification deleted successfully'})
    
    def _send_notification_async(self, notification):
        notification.is_sent = True
        notification.save()

class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['notification_type', 'is_active']
    search_fields = ['name', 'subject_template', 'message_template']
    
    def get_queryset(self):
        if self.request.user.user_type == 'ADMIN':
            return NotificationTemplate.objects.all()
        else:
            return NotificationTemplate.objects.filter(is_active=True)
    
    def create(self, request, *args, **kwargs):
        if request.user.user_type != 'ADMIN':
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        if request.user.user_type != 'ADMIN':
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if request.user.user_type != 'ADMIN':
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        if request.user.user_type != 'ADMIN':
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        template = get_object_or_404(NotificationTemplate, pk=pk)
        template.is_active = not template.is_active
        template.save()
        return Response({
            'message': f'Template {"activated" if template.is_active else "deactivated"} successfully',
            'is_active': template.is_active
        })
    
    @action(detail=True, methods=['post'])
    def preview_template(self, request, pk=None):
        template = get_object_or_404(NotificationTemplate, pk=pk)
        context_data = request.data.get('context', {})
        subject = template.subject_template
        message = template.message_template
        
        for key, value in context_data.items():
            placeholder = f"{{{key}}}"
            subject = subject.replace(placeholder, str(value))
            message = message.replace(placeholder, str(value))
        
        return Response({
            'subject': subject,
            'message': message,
            'template_name': template.name
        })
    
    @action(detail=False, methods=['post'])
    def create_from_template(self, request):
        template_id = request.data.get('template_id')
        context_data = request.data.get('context', {})
        recipient_id = request.data.get('recipient_id')
        
        if not all([template_id, recipient_id]):
            return Response(
                {'error': 'template_id and recipient_id are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        template = get_object_or_404(NotificationTemplate, pk=template_id, is_active=True)
        recipient = get_object_or_404(User, pk=recipient_id)
        
        subject = template.subject_template
        message = template.message_template
        
        for key, value in context_data.items():
            placeholder = f"{{{key}}}"
            subject = subject.replace(placeholder, str(value))
            message = message.replace(placeholder, str(value))
        
        notification = Notification.objects.create(
            recipient=recipient,
            sender=request.user,
            notification_type=template.notification_type,
            title=subject,
            message=message,
            priority=request.data.get('priority', 'MEDIUM'),
            send_email=request.data.get('send_email', False),
            send_sms=request.data.get('send_sms', False),
            send_push=request.data.get('send_push', True)
        )
        self._send_notification_async(notification)
        
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def _send_notification_async(self, notification):
        """Trigger async notification sending"""
        notification.is_sent = True
        notification.save()