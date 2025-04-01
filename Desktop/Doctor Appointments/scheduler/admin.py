from django.contrib import admin
from scheduler.models import Doctor, Patient, Appointment, Availability, MedicalRecord
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Availability)
admin.site.register(MedicalRecord)