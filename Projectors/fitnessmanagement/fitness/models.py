from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Membership(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
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

class Schedules(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False, blank=False)


class Category(models.Model):
    name = models.CharField(max_length=50, null=False)
    BMI = models.FloatField(null=False)

    def __str__(self):
        return self.name

class Fitness_class(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    schedule = models.ForeignKey(Schedules, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category) 
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    max_capacity = models.IntegerField(null=False) 

    def __str__(self):
        return self.name
