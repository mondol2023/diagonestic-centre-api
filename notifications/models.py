from django.db import models
from django.utils import timezone
from accounts.models import User

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('APPOINTMENT', 'Appointment'),
        ('REPORT', 'Report'),
        ('PAYMENT', 'Payment'),
        ('SYSTEM', 'System'),
        ('REMINDER', 'Reminder'),
    )
    
    PRIORITY_LEVELS = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', null=True, blank=True)
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='MEDIUM')
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    
    send_email = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    send_push = models.BooleanField(default=True)
    
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    read_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.recipient.get_full_name()}"

class NotificationTemplate(models.Model):
    name = models.CharField(max_length=100)
    notification_type = models.CharField(max_length=20)
    subject_template = models.CharField(max_length=200)
    message_template = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name