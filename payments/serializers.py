from rest_framework import serializers
from .models import Payment,  Process, PaymentRefund

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process 
        fields = '__all__'
        read_only_fields = ('balance_amount', 'created_at', 'updated_at')

class PaymentSerializer(serializers.ModelSerializer):
    process = ProcessSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('created_at', 'payment_date')

class PaymentRefundSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = PaymentRefund
        fields = '__all__'
        read_only_fields = ('refund_date', 'processed_by')


