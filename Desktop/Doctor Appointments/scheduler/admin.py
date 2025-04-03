from django.contrib import admin
from scheduler.models import Doctor, Patient, Appointment, Availability, MedicalRecord
from django.http.request import HttpRequest
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id','patient_id','doctor_id','day','scheduled_time','duration','end_time','status')
    # adding search fields
    search_fields = ['patient_id']
    # list_filter = ['company_name']
     
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id','first_name','last_name','specialization','phone_no','email','availability_status','created_at')
    # adding search fields
    search_fields = ['specialization']
    # list_filter = ['company_name']
          
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id','first_name','last_name','phone_no','email','date_of_birth','insurance_name','insurance_number')
    # adding search fields
    search_fields = ['insurance_id']
    list_filter = ['patient_id']

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('medicalrecord_id','patient','doctor','record_date','diagnosis','prescription','notes','timestamp')
    # adding search fields
    search_fields = ['diagnosis']
    # list_filter = ['doctor']

admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(Availability)