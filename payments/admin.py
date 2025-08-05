from django.contrib import admin
from .models import Process, Payment, PaymentRefund

# Register your models here.
@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = (
        'process_id', 'patient', 'appointment', 'subtotal', 'discount_amount',
        'tax_amount', 'total_amount', 'paid_amount', 'balance_amount_display',
        'status', 'due_date', 'created_by', 'created_at'
    )
    list_filter = ('status', 'due_date', 'created_at')
    search_fields = (
        'process_id', 'patient__username', 'appointment__appointment_id', 'created_by__username'
    )
    ordering = ('-created_at',)
    autocomplete_fields = ['patient', 'appointment', 'created_by']
    date_hierarchy = 'due_date'
    readonly_fields = ('balance_amount_display',)

    def balance_amount_display(self, obj):
        return obj.balance_amount
    balance_amount_display.short_description = 'Balance Amount'
    balance_amount_display.admin_order_field = 'total_amount'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payment_id', 'process', 'amount', 'payment_method', 'payment_status',
        'transaction_id', 'reference_number', 'payment_date', 'processed_by'
    )
    list_filter = ('payment_method', 'payment_status', 'payment_date')
    search_fields = (
        'payment_id', 'process__process_id', 'transaction_id', 'reference_number', 'processed_by__username'
    )
    ordering = ('-payment_date',)
    autocomplete_fields = ['process', 'processed_by']
    date_hierarchy = 'payment_date'

@admin.register(PaymentRefund)
class PaymentRefundAdmin(admin.ModelAdmin):
    list_display = (
        'payment', 'refund_amount', 'refund_reason', 'refund_date', 'processed_by'
    )
    search_fields = (
        'payment__payment_id', 'refund_reason', 'processed_by__username'
    )
    ordering = ('-refund_date',)
    autocomplete_fields = ['payment', 'processed_by']
    date_hierarchy = 'refund_date'