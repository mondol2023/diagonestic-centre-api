from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import models
from django.db.models import Sum, Q , Count
from .models import Supplier, ItemCategory, Item, Stock
from .serializers import (
    SupplierSerializer, ItemCategorySerializer, ItemSerializer, StockSerializer
)

# Create your views here.
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.filter(is_active=True)
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.request.user.user_type not in ['ADMIN', 'RECEPTIONIST']:
            return [IsAuthenticated()]  
        return [IsAuthenticated()]

class ItemCategoryViewSet(viewsets.ModelViewSet):
    queryset = ItemCategory.objects.all()
    serializer_class = ItemCategorySerializer
    permission_classes = [IsAuthenticated]

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Item.objects.filter(is_active=True)
        
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__id=category)
        
        item_type = self.request.query_params.get('item_type', None)
        if item_type:
            queryset = queryset.filter(item_type=item_type)
        
        stock_status = self.request.query_params.get('stock_status', None)
        if stock_status == 'low':
            queryset = queryset.filter(current_stock__lte=models.F('minimum_stock'))
        elif stock_status == 'out':
            queryset = queryset.filter(current_stock=0)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def low_stock_items(self, request):
        low_stock = Item.objects.filter(
            current_stock__lte=models.F('minimum_stock'),
            is_active=True
        )
        serializer = self.get_serializer(low_stock, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expiring_items(self, request):
        next_month = timezone.now().date() + timezone.timedelta(days=30)
        expiring = Item.objects.filter(
            expiry_date__lte=next_month,
            expiry_date__gt=timezone.now().date(),
            is_active=True
        )
        serializer = self.get_serializer(expiring, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def stock_in(self, request, pk=None):
        if request.user.user_type not in ['ADMIN', 'RECEPTIONIST']:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        item = get_object_or_404(Item, pk=pk)
        quantity = int(request.data.get('quantity', 0))
        unit_price = float(request.data.get('unit_price', item.unit_price))
        reference_number = request.data.get('reference_number', '')
        notes = request.data.get('notes', '')
        
        if quantity <= 0:
            return Response({'error': 'Quantity must be positive'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        transaction = Stock.objects.create(
            item=item,
            transaction_type='IN',
            quantity=quantity,
            unit_price=unit_price,
            total_amount=quantity * unit_price,
            reference_number=reference_number,
            notes=notes,
            created_by=request.user
        )
        
        item.current_stock += quantity
        item.save()
        
        return Response({
            'message': f'Added {quantity} units to {item.name}',
            'new_stock': item.current_stock
        })
    
    @action(detail=True, methods=['post'])
    def stock_out(self, request, pk=None):
        if request.user.user_type not in ['ADMIN', 'RECEPTIONIST', 'LAB_TECH']:
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        
        item = get_object_or_404(Item, pk=pk)
        quantity = int(request.data.get('quantity', 0))
        notes = request.data.get('notes', '')
        
        if quantity <= 0:
            return Response({'error': 'Quantity must be positive'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if quantity > item.current_stock:
            return Response({'error': 'Insufficient stock'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        transaction = Stock.objects.create(
            item=item,
            transaction_type='OUT',
            quantity=quantity,
            unit_price=item.unit_price,
            total_amount=quantity * item.unit_price,
            notes=notes,
            created_by=request.user
        )
        
        item.current_stock -= quantity
        item.save()
        
        return Response({
            'message': f'Removed {quantity} units from {item.name}',
            'new_stock': item.current_stock
        })

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.user_type not in ['ADMIN', 'RECEPTIONIST']:
            return Stock.objects.none()
        
        queryset = Stock.objects.all()
        
        item_id = self.request.query_params.get('item_id', None)
        if item_id:
            queryset = queryset.filter(item__id=item_id)
        
        transaction_type = self.request.query_params.get('transaction_type', None)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        return queryset.order_by('-transaction_date')
    
    @action(detail=False, methods=['get'])
    def transaction_summary(self, request):
        queryset = self.get_queryset()
        
        summary = {}
        for trans_type, _ in Stock.TRANSACTION_TYPES:
            type_transactions = queryset.filter(transaction_type=trans_type)
            summary[trans_type.lower()] = {
                'count': type_transactions.count(),
                'total_amount': float(type_transactions.aggregate(
                    total=Sum('total_amount')
                )['total'] or 0)
            }
        
        return Response(summary)