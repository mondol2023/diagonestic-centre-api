from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Q
from decimal import Decimal
from .models import Pay, Payment, PaymentRefund
from .serializers import PaySerializer, PaymentSerializer, PaymentRefundSerializer

# Create your views here.
class ProcessViewSet(viewsets.ModelViewSet):
    serializer_class = ProcessSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Process.objects.all()
        
        if user.user_type == 'PATIENT':
            queryset = queryset.filter(patient=user)
        elif user.user_type not in ['ADMIN', 'RECEPTIONIST']:
            queryset = queryset.none()
        
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['get'])
    def payment_history(self, request, pk=None):
        pay = get_object_or_404(Process, pk=pk)
        payments = pay.payments.all().order_by('-payment_date')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue_invoices(self, request):
        if request.user.user_type not in ['ADMIN', 'RECEPTIONIST']:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        today = timezone.now().date()
        overdue = Process.objects.filter(
            due_date__lt=today,
            status__in=['PENDING', 'PARTIALLY_PAID']
        )
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def revenue_summary(self, request):
        if request.user.user_type not in ['ADMIN', 'RECEPTIONIST']:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        today = timezone.now().date()
        
        today_revenue = Payment.objects.filter(
            payment_date__date=today,
            payment_status='COMPLETED'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        month_start = today.replace(day=1)
        month_revenue = Payment.objects.filter(
            payment_date__date__gte=month_start,
            payment_status='COMPLETED'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        pending_amount = Process.objects.filter(
            status__in=['PENDING', 'PARTIALLY_PAID']
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        return Response({
            'today_revenue': today_revenue,
            'month_revenue': month_revenue,
            'pending_amount': pending_amount,
            'total_invoices': Pay.objects.count(),
            'paid_invoices': Pay.objects.filter(status='PAID').count()
        })

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Payment.objects.all()
        
        if user.user_type == 'PATIENT':
            queryset = queryset.filter(invoice__patient=user)
        elif user.user_type not in ['ADMIN', 'RECEPTIONIST']:
            queryset = queryset.none()
        
        return queryset.order_by('-payment_date')
    
    def create(self, request, *args, **kwargs):
        if request.user.user_type not in ['ADMIN', 'RECEPTIONIST']:
            return Response({'error': 'Only authorized staff can process payments'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            payment = serializer.save(processed_by=request.user)
            
            invoice = payment.invoice
            invoice.paid_amount += payment.amount
            
            if invoice.paid_amount >= invoice.total_amount:
                invoice.status = 'PAID'
            elif invoice.paid_amount > 0:
                invoice.status = 'PARTIALLY_PAID'
            
            invoice.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def process_refund(self, request, pk=None):
        if request.user.user_type not in ['ADMIN']:
            return Response({'error': 'Only admins can process refunds'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        payment = get_object_or_404(Payment, pk=pk)
        if payment.payment_status != 'COMPLETED':
            return Response({'error': 'Only completed payments can be refunded'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        refund_amount = Decimal(request.data.get('refund_amount', 0))
        refund_reason = request.data.get('refund_reason', '')
        
        if refund_amount <= 0 or refund_amount > payment.amount:
            return Response({'error': 'Invalid refund amount'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        refund = PaymentRefund.objects.create(
            payment=payment,
            refund_amount=refund_amount,
            refund_reason=refund_reason,
            processed_by=request.user
        )
        payment.payment_status = 'REFUNDED'
        payment.save()
        
        pay = payment.pay
        pay.paid_amount -= refund_amount
        if pay.paid_amount < pay.total_amount:
            pay.status = 'PARTIALLY_PAID' if pay.paid_amount > 0 else 'PENDING'
        pay.save()

        return Response({'message': 'Refund processed successfully'})

class PaymentRefundViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PaymentRefund.objects.all()
    serializer_class = PaymentRefundSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type not in ['ADMIN', 'RECEPTIONIST']:
            return PaymentRefund.objects.none()
        return PaymentRefund.objects.all().order_by('-refund_date')