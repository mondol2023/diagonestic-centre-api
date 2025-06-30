from django.contrib import admin
from .models import TestCategory, Test, TestPackage

# Register your models here.
@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'code', 'category', 'test_type', 'price',
        'duration_hours', 'is_active'
    )
    list_filter = ('test_type', 'category', 'is_active')
    search_fields = ('name', 'code', 'category__name', 'preparation_instructions')
    ordering = ('name',)
    autocomplete_fields = ['category']
    list_editable = ('is_active',)

@admin.register(TestPackage)
class TestPackageAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'discount_percentage', 'total_tests_display', 'is_active'
    )
    list_filter = ('is_active',)
    search_fields = ('name', 'description', 'tests__name')
    filter_horizontal = ('tests',)
    ordering = ('name',)

    def total_tests_display(self, obj):
        return obj.total_tests
    total_tests_display.short_description = "Total Tests"
