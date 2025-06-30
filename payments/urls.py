from django.urls import path
from . import views

urlpatterns = [
    path(
        'pays/',
        views.PayViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='pay-list'
    ),
    path(
        'pays/<int:pk>/',
        views.PayViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='pay-detail'
    ),
    path(
        'pays/<int:pk>/payment_history/',
        views.PayViewSet.as_view({'get': 'payment_history'}),
        name='pay-payment-history'
    ),
    path(
        'pays/overdue_invoices/',
        views.PayViewSet.as_view({'get': 'overdue_invoices'}),
        name='pay-overdue-invoices'
    ),
    path(
        'pays/revenue_summary/',
        views.PayViewSet.as_view({'get': 'revenue_summary'}),
        name='pay-revenue-summary'
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