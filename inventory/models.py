from django.db import models
from django.utils import timezone
from accounts.models import User

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ItemCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Item(models.Model):
    ITEM_TYPES = (
        ('CONSUMABLE', 'Consumable'),
        ('EQUIPMENT', 'Equipment'),
        ('REAGENT', 'Reagent'),
        ('MEDICINE', 'Medicine'),
    )
    
    item_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    
    current_stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=0)
    maximum_stock = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    brand = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock
    
    def __str__(self):
        return f"{self.item_code} - {self.name}"

class Stock(models.Model):
    TRANSACTION_TYPES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJUSTMENT', 'Adjustment'),
        ('DAMAGED', 'Damaged'),
        ('EXPIRED', 'Expired'),
    )
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    reference_type = models.CharField(max_length=50, blank=True)  
    reference_number = models.CharField(max_length=100, blank=True)
    
    notes = models.TextField(blank=True)
    transaction_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.item.name} - {self.transaction_type} - {self.quantity}"