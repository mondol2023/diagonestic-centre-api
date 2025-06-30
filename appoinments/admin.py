from django.contrib import admin
from .models import Appointment, AppointmentHistory

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'appointment_id',
        'patient',
        'doctor',
        'appointment_type',
        'appointment_date',
        'appointment_time',
        'status',
        'created_by',
    )
    list_filter = (
        'appointment_type',
        'status',
        'appointment_date',
    )
    search_fields = (
        'appointment_id',
        'patient__username',
        'doctor__username',
        'created_by__username',
        'notes',
    )
    autocomplete_fields = ['patient', 'doctor', 'created_by', 'tests', 'test_packages']
    ordering = ['-appointment_date', '-appointment_time']
    date_hierarchy = 'appointment_date'
    filter_horizontal = ['tests', 'test_packages']

@admin.register(AppointmentHistory)
class AppointmentHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'appointment',
        'status_changed_from',
        'status_changed_to',
        'changed_by',
        'timestamp',
    )
    search_fields = (
        'appointment__appointment_id',
        'changed_by__username',
        'status_changed_from',
        'status_changed_to',
    )
    list_filter = (
        'status_changed_to',
        'timestamp',
    )
    autocomplete_fields = ['appointment', 'changed_by']
    date_hierarchy = 'timestamp'