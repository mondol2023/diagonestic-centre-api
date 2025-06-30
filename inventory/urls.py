from django.urls import path
from . import views

urlpatterns = [
    path(
        'suppliers/',
        views.SupplierViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='supplier-list'
    ),
    path(
        'suppliers/<int:pk>/',
        views.SupplierViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='supplier-detail'
    ),
    path(
        'item-categories/',
        views.ItemCategoryViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='itemcategory-list'
    ),
    path(
        'item-categories/<int:pk>/',
        views.ItemCategoryViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='itemcategory-detail'
    ),
    path(
        'items/',
        views.ItemViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='item-list'
    ),
    path(
        'items/<int:pk>/',
        views.ItemViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='item-detail'
    ),
    path(
        'items/low_stock_items/',
        views.ItemViewSet.as_view({'get': 'low_stock_items'}),
        name='item-low-stock'
    ),
    path(
        'items/expiring_items/',
        views.ItemViewSet.as_view({'get': 'expiring_items'}),
        name='item-expiring'
    ),
    path(
        'items/<int:pk>/stock_in/',
        views.ItemViewSet.as_view({'post': 'stock_in'}),
        name='item-stock-in'
    ),
    path(
        'items/<int:pk>/stock_out/',
        views.ItemViewSet.as_view({'post': 'stock_out'}),
        name='item-stock-out'
    ),
    path(
        'stock/',
        views.StockViewSet.as_view({'get': 'list'}), 
        name='stock-list'
    ),
    path(
        'stock/<int:pk>/',
        views.StockViewSet.as_view({'get': 'retrieve'}),
        name='stock-detail'
    ),
    path(
        'stock/transaction_summary/',
        views.StockViewSet.as_view({'get': 'transaction_summary'}),
        name='stock-transaction-summary'
    ),
]