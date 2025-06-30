from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patient, Doctor, LabTechnician, Receptionist

# Custom UserAdmin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": (
                "user_type",
                "name",
                "phone",
                "address",
                "date_of_birth",
                "gender",
                "profile_picture",
                "created_at",
            )
        }),
    )
    list_display = ("username", "email", "user_type", "name", "is_active", "is_staff")
    list_filter = ("user_type", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "name", "phone")
    ordering = ("username",)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("user", "patient_id", "blood_group", "emergency_contact")
    search_fields = ("user__username", "patient_id", "blood_group")
    list_filter = ("blood_group",)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("user", "doctor_id", "specialization", "consultation_fee")
    search_fields = ("user__username", "doctor_id", "specialization", "license_number")
    list_filter = ("specialization",)

@admin.register(LabTechnician)
class LabTechnicianAdmin(admin.ModelAdmin):
    list_display = ("user", "tech_id", "specialization", "shift_timing")
    search_fields = ("user__username", "tech_id", "specialization")
    list_filter = ("specialization",)

@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ("user", "employee_id", "shift_timing")
    search_fields = ("user__username", "employee_id")
