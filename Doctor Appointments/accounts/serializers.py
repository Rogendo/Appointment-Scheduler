import datetime
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from .models import Doctor,Patient, MedicalRecord, Appointment, Availability
from django.db.models import Q
from.serializers import *
from django.utils import timezone
from datetime import datetime, timedelta
from datetime import datetime, timedelta

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    """
    A login serializer for Logging in the user
    """
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    """
    An authentication serializer for authenticating the user
    """
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "first_name",
            "last_name",
            "bio",
            "phone_number",
            "user_type",
            "password",
            "created_at",
            "updated_at",
            "auth_token",
        ]
        read_only_fields = [
            "id",
            "is_active",
            "is_staff",
        ]
        extra_kwargs = {"password": {"write_only": True}}
   
    def get_auth_token(self, obj):
        try:
            token = Token.objects.get(user=obj)
            token.delete()
        except ObjectDoesNotExist:
            pass
        token = Token.objects.create(user=obj)
        return token.key


class EmptySerializer(serializers.Serializer):
    pass


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "bio",
            "phone_number",
            "user_type",
            "password",
        ]

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password


class PasswordChangeSerializer(serializers.Serializer):
    """
    A user password change serializer for chaning password
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Current password does not match")
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class AccountProfileSerializer(serializers.ModelSerializer):
    """
    A user serializer for the  user profile
    """
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "bio",
            "phone_number",
            "user_type",
        ]


class MedicalRecordSerializer(serializers.ModelSerializer):
    """
    A serializer for the MedicalRecord model
    """
    class Meta:
        model = MedicalRecord
        fields = [
            'medicalrecord_id',
            'appointment' ,
            'diagnosis',
            'prescription',
            'notes'
            ]

class PatientSerializer(serializers.ModelSerializer):
    """
    A patient serializer for registering the patient
    """
    class Meta:
        model = Patient
        fields = [
            'patient_id',
            'first_name',
            'last_name',
            'phone_no',
            'email',
            'date_of_birth',
            'insurance_number',
            'insurance_name',
            'timestamp'
            ]

class DoctorSerializer(serializers.ModelSerializer):
    """"
    A doctor serializer for registering the doctor
    """
    class Meta:
        model = Doctor
        fields = [ 
            'doctor_id',
            'first_name',
            'last_name',
            'specialization',
            'department',
            'email', 
            'created_at',
            'availability_status'
            ]


class AppointmentSerializer(serializers.ModelSerializer):
    """
    A serializer for the Appointment model
    """
    class Meta:
        model = Appointment
        fields = [
            'appointment_id', 
            'patient', 
            'doctor', 
            'date', 
            'scheduled_time', 
            'duration', 
            'status', 
            'end_time', 
            "availability"
            ]
        read_only_fields = ['end_time']

    def validate(self, data):
        # Calculate appointment end time
        start = datetime.combine(data['date'], data['scheduled_time'])
        end = start + timedelta(minutes=data['duration'])
        data['end_time'] = end.time()

        # Check if within ANY availability slot
        is_available = Availability.objects.filter(
            doctor=data['doctor'],
            date=data['date'],
            start_time__lte=data['scheduled_time'],
            end_time__gte=end.time(),
            available=True
        ).exists()

        if not is_available:
            raise serializers.ValidationError("Doctor is not available during this time.")

        # Check for overlapping appointments
        overlapping_appointments = Appointment.objects.filter(
            doctor=data['doctor'],
            date=data['date'],
            scheduled_time__lt=end.time(),
            end_time__gt=data['scheduled_time']
        ).exists()

        if overlapping_appointments:
            raise serializers.ValidationError("Time slot is already booked.")

        return data
    
    def create(self, validated_data):
        # Find and update the availability slot
        slot = Availability.objects.get(
            doctor=validated_data['doctor'],
            date=validated_data['date'],
            start_time__lte=validated_data['scheduled_time'],
            end_time__gte=validated_data['end_time'],
            available=True
        )
        slot.available = False
        slot.save()

        # Create the appointment
        return super().create(validated_data)        

class AvailabilitySerializer(serializers.ModelSerializer):
    """
    A serializer for the Availability model
    """
    class Meta:
        model = Availability
        fields = [
            'doctor', 
            'date', 
            'start_time', 
            'end_time', 
            'available'
            ]

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        return data
    
def split_into_sessions(availability):
    """
    Given an Availability instance, split its timeslot into one-hour sessions.
    Returns a list of tuples: [(session_start, session_end), ...]
    """
    sessions = []
    # Assume availability.date is a date object and start_time/end_time are time objects.
    start = datetime.combine(availability.date, availability.start_time)
    end = datetime.combine(availability.date, availability.end_time)
    
    while start + timedelta(hours=1) <= end:
        session_end = start + timedelta(hours=1)
        sessions.append((start.time(), session_end.time()))
        start += timedelta(hours=1)
    
    return sessions