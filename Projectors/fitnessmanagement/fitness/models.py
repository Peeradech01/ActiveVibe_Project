from django.db import models

# Create your models here.

class Membership(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=100, null=False)
    price = models.FloatField(null=False)
    duration = models.IntegerField(null=False)

    def __str__(self):
        return self.name
    