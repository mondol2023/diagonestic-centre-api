from django.db import models
from django.utils import timezone
from accounts.models import User
from appoinments.models import Appointment

# Create your models here.
class Pay(models.Model):
    PAY_STATUS = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    )
    pay_id = models.CharField(max_length=20, unique=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pay')
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=PAY_STATUS, default='PENDING')
    due_date = models.DateField()

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_pays')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def balance_amount(self):
        return self.total_amount - self.paid_amount
    
    def __str__(self):
        return f"Pay {self.pay_id} - {self.patient.get_full_name()}"

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('UPI', 'UPI'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
    )
    
    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )
    
    payment_id = models.CharField(max_length=20, unique=True)
    pay = models.ForeignKey(Pay, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    
    transaction_id = models.CharField(max_length=100, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(default=timezone.now)
    
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processed_payments')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Payment {self.payment_id} - ₹{self.amount}"

class PaymentRefund(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_reason = models.TextField()
    refund_date = models.DateTimeField(default=timezone.now)
    processed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Refund for {self.payment.payment_id}"
