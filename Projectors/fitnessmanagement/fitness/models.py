from django.db import models
from django.conf import settings
from django.utils import timezone

class Membership(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    price = models.FloatField(null=False)
    duration = models.IntegerField(null=False)

    def __str__(self):
        return self.name

class CustomerMembership(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)

class PersonalInfo(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    customer = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE) 
    trainer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='fitness_classes')
    start_time = models.DateTimeField(null=False, blank=False, default=None)
    end_time = models.DateTimeField(null=False, blank=False, default=None)
    max_capacity = models.IntegerField(null=False) 

    def __str__(self):
        return self.name