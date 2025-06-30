from django.contrib import admin
from .models import TestReport, TestParameter, ReportTemplate

# Register your models here.
@admin.register(TestReport)
class TestReportAdmin(admin.ModelAdmin):
    list_display = (
        'report_id', 'appointment', 'patient', 'test', 'lab_technician',
        'verified_by', 'test_date', 'report_date', 'status', 'created_at'
    )
    list_filter = ('status', 'test_date', 'report_date', 'created_at')
    search_fields = (
        'report_id', 'patient__username', 'lab_technician__username',
        'verified_by__username', 'test__name', 'appointment__appointment_id'
    )
    autocomplete_fields = ['appointment', 'patient', 'test', 'lab_technician', 'verified_by']
    date_hierarchy = 'test_date'
    ordering = ('-test_date',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(TestParameter)
class TestParameterAdmin(admin.ModelAdmin):
    list_display = (
        'test', 'parameter_name', 'unit', 'normal_range_min',
        'normal_range_max', 'normal_range_text'
    )
    search_fields = ('parameter_name', 'test__name')
    list_filter = ('test',)
    autocomplete_fields = ['test']
    ordering = ('test__name', 'parameter_name')

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'test', 'is_active')
    search_fields = ('name', 'test__name')
    list_filter = ('is_active',)
    autocomplete_fields = ['test']
    ordering = ('name',)


