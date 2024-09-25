from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Membership(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=100, null=False)
    price = models.FloatField(null=False)
    duration = models.IntegerField(null=False)

    def __str__(self):
        return self.name
    
class Personal_info(models.Model):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('trainer', 'Trainer'),
        ('manager', 'Manager')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(null=False, default=0)
    height = models.FloatField(null=False, default=0)
    BMI = models.FloatField(null=False, default=0)
    phone = models.CharField(max_length=10, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    

