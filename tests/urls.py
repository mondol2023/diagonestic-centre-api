from django.urls import path
from . import views

urlpatterns = [
    path(
        'test-categories/',
        views.TestCategoryViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='testcategory-list'
    ),
    path(
        'test-categories/<int:pk>/',
        views.TestCategoryViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='testcategory-detail'
    ),
    path(
        'tests/',
        views.TestViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='test-list'
    ),
    path(
        'tests/<int:pk>/',
        views.TestViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='test-detail'
    ),
    path(
        'tests/popular/', 
        views.TestViewSet.as_view({'get': 'popular_tests'}),
        name='test-popular'
    ),
    path(
        'tests/<int:pk>/parameters/', 
        views.TestViewSet.as_view({'get': 'parameters'}),
        name='test-parameters'
    ),
    path(
        'test-packages/',
        views.TestPackageViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='testpackage-list'
    ),
    path(
        'test-packages/<int:pk>/',
        views.TestPackageViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='testpackage-detail'
    ),
    path(
        'test-packages/<int:pk>/calculate_savings/', 
        views.TestPackageViewSet.as_view({'get': 'calculate_savings'}),
        name='testpackage-calculate-savings'
    ),
]