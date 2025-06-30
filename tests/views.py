from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import TestCategory, Test, TestPackage
from .serializers import TestCategorySerializer, TestSerializer, TestPackageSerializer

# Create your views here.
class TestCategoryViewSet(viewsets.ModelViewSet):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]  

class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Test.objects.filter(is_active=True)
        
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)
        
        test_type = self.request.query_params.get('test_type', None)
        if test_type:
            queryset = queryset.filter(test_type=test_type)
        
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def popular_tests(self, request):
        popular_tests = Test.objects.filter(is_active=True)[:10]
        serializer = self.get_serializer(popular_tests, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def parameters(self, request, pk=None):
        test = get_object_or_404(Test, pk=pk)
        parameters = test.parameters.all()
        from reports.serializers import TestParameterSerializer
        serializer = TestParameterSerializer(parameters, many=True)
        return Response(serializer.data)

class TestPackageViewSet(viewsets.ModelViewSet):
    queryset = TestPackage.objects.filter(is_active=True)
    serializer_class = TestPackageSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def calculate_savings(self, request, pk=None):
        package = get_object_or_404(TestPackage, pk=pk)
        individual_total = sum(test.price for test in package.tests.all())
        savings = individual_total - package.price
        savings_percentage = (savings / individual_total) * 100 if individual_total > 0 else 0
        
        return Response({
            'individual_total': individual_total,
            'package_price': package.price,
            'savings': savings,
            'savings_percentage': round(savings_percentage, 2)
        })