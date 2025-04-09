from django.contrib import admin
from .models import CustomUser
from .models import Doctor, Patient, Appointment, Availability, MedicalRecord
from django.http.request import HttpRequest
from django.contrib.auth.admin import UserAdmin


admin.site.site_header = "Scheduler Admin"
admin.site.site_title = "Scheduler Admin"
admin.site.index_title = "Scheduler Admin"

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'date', 'scheduled_time', 'duration', 'status', 'end_time', 'created_at')
    # adding search fields
    search_fields = ['patient_id']
    list_filter = ['appointment_id']
    
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id','doctor','date','start_time','end_time','available')
    # adding search fields
    search_fields = ['doctor']
    list_filter = ['doctor']
     
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id','first_name','last_name','specialization','email','availability_status','created_at')
    # adding search fields
    search_fields = ['specialization']
    list_filter = ['last_name']
          
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id','first_name','last_name','phone_no','email','date_of_birth','insurance_name','insurance_number')
    # adding search fields
    search_fields = ['insurance_id']
    list_filter = ['patient_id']

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('medicalrecord_id','appointment','record_date','diagnosis','prescription','notes')
    # adding search fields
    search_fields = ['diagnosis']
    list_filter = ['medicalrecord_id']

admin.site.register(Doctor,DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(Availability,AvailabilityAdmin)


admin.site.register(
    CustomUser
    )