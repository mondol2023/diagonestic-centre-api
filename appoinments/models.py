from django.db import models
from django.utils import timezone
from accounts.models import User
from tests.models import Test, TestPackage

# Create your models here.
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    )
    
    APPOINTMENT_TYPES = (
        ('CONSULTATION', 'Consultation'),
        ('TEST', 'Test'),
        ('FOLLOW_UP', 'Follow Up'),
    )
    
    appointment_id = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments', null=True, blank=True)
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    tests = models.ManyToManyField(Test, blank=True)
    test_packages = models.ManyToManyField(TestPackage, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_appointments')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['appointment_date', 'appointment_time']
    
    def __str__(self):
        return f"{self.appointment_id} - {self.patient.get_full_name()} on {self.appointment_date}"

class AppointmentHistory(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='history')
    status_changed_from = models.CharField(max_length=20)
    status_changed_to = models.CharField(max_length=20)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)