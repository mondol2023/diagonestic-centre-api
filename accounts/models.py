from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    USER_TYPES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('LAB_TECH', 'Lab Technician'),
        ('RECEPTIONIST', 'Receptionist'),
        ('ADMIN', 'Admin'),
    )    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='PATIENT')
    name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    patient_id = models.CharField(max_length=20, unique=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"Patient: {self.user.get_full_name()}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    doctor_id = models.CharField(max_length=20, unique=True)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    qualification = models.TextField()
    experience_years = models.IntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    available_days = models.CharField(max_length=50, help_text="e.g., Mon,Tue,Wed")
    available_time_start = models.TimeField()
    available_time_end = models.TimeField()
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"

class LabTechnician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='lab_tech')
    tech_id = models.CharField(max_length=20, unique=True)
    specialization = models.CharField(max_length=100)
    certification = models.TextField()
    shift_timing = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Tech: {self.user.get_full_name()}"

class Receptionist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='receptionist')
    employee_id = models.CharField(max_length=20, unique=True)
    shift_timing = models.CharField(max_length=20)
    
    def __str__(self):
        return f"Receptionist: {self.user.get_full_name()}"