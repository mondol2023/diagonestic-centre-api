from django.urls import path
from . import views

urlpatterns = [
    path(
        'test-reports/',
        views.TestReportViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='testreport-list'
    ),
    path(
        'test-reports/<int:pk>/',
        views.TestReportViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='testreport-detail'
    ),
    path(
        'test-reports/<int:pk>/add_results/',
        views.TestReportViewSet.as_view({'post': 'add_results'}),
        name='testreport-add-results'
    ),
    path(
        'test-reports/<int:pk>/verify/',
        views.TestReportViewSet.as_view({'post': 'verify_report'}),
        name='testreport-verify'
    ),
    path(
        'test-reports/<int:pk>/download_pdf/',
        views.TestReportViewSet.as_view({'get': 'download_pdf'}),
        name='testreport-download-pdf'
    ),
    path(
        'test-reports/pending/',
        views.TestReportViewSet.as_view({'get': 'pending_reports'}),
        name='testreport-pending'
    ),
    path(
        'test-reports/for_verification/',
        views.TestReportViewSet.as_view({'get': 'reports_for_verification'}),
        name='testreport-for-verification'
    ),
    path(
        'test-parameters/',
        views.TestParameterViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='testparameter-list'
    ),
    path(
        'test-parameters/<int:pk>/',
        views.TestParameterViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='testparameter-detail'
    ),
    path(
        'report-templates/',
        views.ReportTemplateViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='reporttemplate-list'
    ),
    path(
        'report-templates/<int:pk>/',
        views.ReportTemplateViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='reporttemplate-detail'
    ),
]