from django.db import models
from django.utils import timezone
from accounts.models import User
from tests.models import Test
from appoinments.models import Appointment

# Create your models here.
class TestReport(models.Model):
    REPORT_STATUS = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('VERIFIED', 'Verified'),
        ('DELIVERED', 'Delivered'),
    )
    
    report_id = models.CharField(max_length=20, unique=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_reports')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    lab_technician = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conducted_tests')
    verified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verified_reports', null=True, blank=True)
    
    test_date = models.DateTimeField(default=timezone.now)
    report_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='PENDING')
    
    results = models.JSONField(default=dict, help_text="Store test parameter results")
    interpretation = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)
    images = models.JSONField(default=list, help_text="Store image URLs")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.report_id} - {self.patient.get_full_name()} - {self.test.name}"

class TestParameter(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='parameters')
    parameter_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, blank=True)
    normal_range_min = models.FloatField(null=True, blank=True)
    normal_range_max = models.FloatField(null=True, blank=True)
    normal_range_text = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.test.name} - {self.parameter_name}"

class ReportTemplate(models.Model):
    name = models.CharField(max_length=100)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    template_content = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.test.name}"