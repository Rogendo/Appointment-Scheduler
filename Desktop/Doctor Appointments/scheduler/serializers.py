from rest_framework import serializers
from scheduler.models import Doctor,Patient, MedicalRecord, Appointment, Availability, Session

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['medicalrecord_id','patient','appointment','doctor','record_date']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['patient_id', 'doctor_id', 'start_time', 'end_time', 'status']

# class AppointmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Appointment
#         fields = ['doctor', 'start_time', 'end_time']

# class SessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Session
#         fields = ['patient', 'doctor', 'start_time', 'end_time']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['patient_id', 'doctor_id', 'start_time', 'end_time']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patient_id','first_name','last_name','phone_no','email','date_of_birth','insurance_number', 'insurance_name','timestamp']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['doctor_id','first_name','last_name','specialization','phone_no','email', 'created_at']