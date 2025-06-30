from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Q
from .models import TestReport, TestParameter, ReportTemplate
from .serializers import TestReportSerializer, TestParameterSerializer, ReportTemplateSerializer
import json

# Create your views here.
class TestReportViewSet(viewsets.ModelViewSet):
    serializer_class = TestReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = TestReport.objects.all()
        
        if user.user_type == 'PATIENT':
            queryset = queryset.filter(patient=user)
        elif user.user_type == 'DOCTOR':
            queryset = queryset.filter(
                Q(verified_by=user) | Q(appointment__doctor=user)
            )
        elif user.user_type == 'LAB_TECH':
            queryset = queryset.filter(lab_technician=user)
        
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(test_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(test_date__lte=end_date)
        
        return queryset.order_by('-test_date')
    
    @action(detail=True, methods=['post'])
    def add_results(self, request, pk=None):
        """Add test results (Lab Technician only)"""
        if request.user.user_type != 'LAB_TECH':
            return Response({'error': 'Only lab technicians can add results'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        report = get_object_or_404(TestReport, pk=pk)
        if report.status not in ['PENDING', 'IN_PROGRESS']:
            return Response({'error': 'Cannot modify completed reports'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        results = request.data.get('results', {})
        interpretation = request.data.get('interpretation', '')
        
        report.results = results
        report.interpretation = interpretation
        report.status = 'COMPLETED'
        report.report_date = timezone.now()
        report.save()
        
        return Response({'message': 'Results added successfully'})
    
    @action(detail=True, methods=['post'])
    def verify_report(self, request, pk=None):
        """Verify report (Doctor only)"""
        if request.user.user_type != 'DOCTOR':
            return Response({'error': 'Only doctors can verify reports'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        report = get_object_or_404(TestReport, pk=pk)
        if report.status != 'COMPLETED':
            return Response({'error': 'Only completed reports can be verified'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        report.verified_by = request.user
        report.status = 'VERIFIED'
        report.recommendations = request.data.get('recommendations', '')
        report.save()
        
        return Response({'message': 'Report verified successfully'})
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Download report as PDF"""
        report = get_object_or_404(TestReport, pk=pk)
        
        user = request.user
        if user.user_type == 'PATIENT' and report.patient != user:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            'report_id': report.report_id,
            'patient': report.patient.get_full_name(),
            'test': report.test.name,
            'results': report.results,
            'interpretation': report.interpretation,
            'recommendations': report.recommendations,
            'test_date': report.test_date,
            'report_date': report.report_date
        })
    
    @action(detail=False, methods=['get'])
    def pending_reports(self, request):
        """Get pending reports for lab technician"""
        if request.user.user_type not in ['LAB_TECH', 'ADMIN']:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        reports = TestReport.objects.filter(
            status__in=['PENDING', 'IN_PROGRESS'],
            lab_technician=request.user
        )
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def reports_for_verification(self, request):
        """Get reports pending verification (Doctor only)"""
        if request.user.user_type != 'DOCTOR':
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        reports = TestReport.objects.filter(status='COMPLETED')
        serializer = self.get_serializer(reports, many=True)
        return Response(serializer.data)

class TestParameterViewSet(viewsets.ModelViewSet):
    queryset = TestParameter.objects.all()
    serializer_class = TestParameterSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        test_id = self.request.query_params.get('test_id', None)
        if test_id:
            return TestParameter.objects.filter(test__id=test_id)
        return TestParameter.objects.all()

class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.filter(is_active=True)
    serializer_class = ReportTemplateSerializer
    permission_classes = [IsAuthenticated]