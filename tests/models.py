from django.db import models
from django.utils import timezone
from accounts.models import User

# Create your models here.
class TestCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Test(models.Model):
    TEST_TYPES = (
        ('BLOOD', 'Blood Test'),
        ('URINE', 'Urine Test'),
        ('IMAGING', 'Imaging'),
        ('PATHOLOGY', 'Pathology'),
        ('BIOCHEMISTRY', 'Biochemistry'),
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=20, choices=TEST_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_hours = models.IntegerField(help_text="Expected completion time in hours")
    preparation_instructions = models.TextField(blank=True)
    normal_range = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class TestPackage(models.Model):
    name = models.CharField(max_length=200)
    tests = models.ManyToManyField(Test)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    @property
    def total_tests(self):
        return self.tests.count()