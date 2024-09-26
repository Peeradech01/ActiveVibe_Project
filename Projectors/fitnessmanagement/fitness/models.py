from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone

# Create your models here.

class Membership(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    price = models.FloatField(null=False)
    duration = models.IntegerField(null=False)

    def __str__(self):
        return self.name
    
class CustomerMembership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)

class PersonalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weight = models.FloatField(null=False, default=0)
    height = models.FloatField(null=False, default=0)
    bmi = models.FloatField(null=False, default=0)
    phone = models.CharField(max_length=10, null=False)


class Category(models.Model):
    name = models.CharField(max_length=50, null=False)
    bmi = models.FloatField(null=False)

    def __str__(self):
        return self.name

class FitnessClass(models.Model):
    user = models.ManyToManyField(User)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, default=None) 
    trainer = models.ForeignKey(Group, on_delete=models.CASCADE, null=False)
    max_capacity = models.IntegerField(null=False) 

    def __str__(self):
        return self.name

class Schedules(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]
    fitnessclass = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, default=None)
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False, blank=False)
