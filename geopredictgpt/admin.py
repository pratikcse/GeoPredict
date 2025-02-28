from django.contrib import admin

# Register your models here.
from .models import Patient, Donation

# Register your models here.
admin.site.register(Patient)
admin.site.register(Donation)