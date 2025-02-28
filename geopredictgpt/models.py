from django.db import models
from django.contrib import admin
class Patient(models.Model):
    STATUS_CHOICES = [
        ('Safe', 'Safe'),
        ('Injured', 'Injured'),
        ('Critical', 'Critical'),
        ('Deceased', 'Deceased'),
    ]

    name = models.CharField(max_length=200)
    patient_id = models.CharField(max_length=50, unique=True)
    current_location = models.CharField(max_length=200)
    rescued_location = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name
    


class Donation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ${self.amount}"


