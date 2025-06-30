from rest_framework import serializers
from .models import Notification, NotificationTemplate
from accounts.models import User

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationTemplateSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    time_since_created = serializers.SerializerMethodField()
    
    class Meta:
        model = NotificationTemplate
        fields = '__all__'