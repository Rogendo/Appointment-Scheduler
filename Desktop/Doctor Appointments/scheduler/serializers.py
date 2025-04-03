from datetime import timezone
from rest_framework import serializers
from scheduler.models import Doctor,Patient, MedicalRecord, Appointment, Availability, Session

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['medicalrecord_id','patient','doctor', 'diagnosis','prescription','notes']

# class AppointmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Appointment
#         fields = ['patient_id', 'doctor_id', 'start_time', 'end_time', 'status']

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
        fields = ['doctor_id','first_name','last_name','specialization','department','phone_no','email', 'created_at','availability_status']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointment_id', 'patient_id', 'doctor_id', 'day','scheduled_time',  'duration', 'status','end_time', 'created_at']
        # extra_kwargs = {
        #     'patient_id': {'required': True},
        #     'doctor_id': {'required': True}
        # }

    def validate(self, data):
        # Check appointment duration
        if data['scheduled_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")
            
        # Check future dates
        if data['date'] < timezone.now().date():
            raise serializers.ValidationError("Cannot book appointments in the past")
            
        return data
    

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['av_id', 'doctor', 'date', 'start_time', 'end_time', 'day_of_week','valid_from','valid_until','available']