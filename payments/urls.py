from django.urls import path
from . import views

urlpatterns = [
    path(
        'process'/',
        views.ProceddViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='process-list'
    ),
    path(
        'process/<int:pk>/',
        views.ProcessViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='process-detail'
    ),
    path(
        'process/<int:pk>/payment_history/',
        views.ProcessViewSet.as_view({'get': 'payment_history'}),
        name='process-payment-history'
    ),
    path(
        'process/overdue_invoices/',
        views.ProcessViewSet.as_view({'get': 'overdue_invoices'}),
        name='process-overdue-invoices'
    ),
    path(
        'process/revenue_summary/',
        views.ProcessViewSet.as_view({'get': 'revenue_summary'}),
        name='process-revenue-summary'
    ),
    path(
        'payments/',
        views.PaymentViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='payment-list'
    ),
    path(
        'payments/<int:pk>/',
        views.PaymentViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='payment-detail'
    ),
    path(
        'payments/<int:pk>/process_refund/',
        views.PaymentViewSet.as_view({'post': 'process_refund'}),
        name='payment-process-refund'
    ),
    path(
        'payment-refunds/',
        views.PaymentRefundViewSet.as_view({'get': 'list'}), 
        name='paymentrefund-list'
    ),
    path(
        'payment-refunds/<int:pk>/',
        views.PaymentRefundViewSet.as_view({'get': 'retrieve'}), 
        name='paymentrefund-detail'
    ),
]