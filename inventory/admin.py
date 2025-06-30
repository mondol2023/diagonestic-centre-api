from django.contrib import admin
from .models import Supplier, ItemCategory, Item, Stock

# Register your models here.
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'email', 'is_active')
    search_fields = ('name', 'contact_person', 'phone', 'email')
    list_filter = ('is_active',)
    ordering = ('name',)

@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'item_code', 'name', 'item_type', 'category', 'supplier',
        'current_stock', 'minimum_stock', 'maximum_stock',
        'unit_price', 'is_low_stock', 'expiry_date', 'is_active'
    )
    list_filter = ('item_type', 'category', 'supplier', 'is_active', 'expiry_date')
    search_fields = ('item_code', 'name', 'brand', 'model_number')
    ordering = ('name',)
    readonly_fields = ('is_low_stock',)
    autocomplete_fields = ['category', 'supplier']

    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True
    is_low_stock.short_description = "Low Stock?"

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'item', 'transaction_type', 'quantity', 'unit_price',
        'total_amount', 'reference_type', 'reference_number',
        'transaction_date', 'created_by'
    )
    list_filter = ('transaction_type', 'transaction_date')
    search_fields = ('item__name', 'reference_number', 'created_by__username')
    autocomplete_fields = ['item', 'created_by']
    date_hierarchy = 'transaction_date'
    ordering = ('-transaction_date',)