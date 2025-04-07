import datetime
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from .models import Doctor,Patient, MedicalRecord, Appointment, Availability
from.serializers import *
from django.utils import timezone

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
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
        fields = ['appointment_id', 'patient_id', 'doctor_id', 'day','scheduled_time',  'timestamp','duration', 'status','end_time', 'created_at']
        # extra_kwargs = {
        #     'patient_id': {'required': True},
        #     'doctor_id': {'required': True}
        # }

    def validate(self, data):
        # Check appointment duration
        if data['scheduled_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")
            
        
        current_day = datetime.datetime.today().strftime('%A')
        # Convert `day` numeric to string
        day_map = {
            '1': 'Monday',
            '2': 'Teusday',  
            '3': 'Wednesday',
            '4': 'Thurday', 
            '5': 'Friday',
            '6':'Saturday',
            '7':'Sunday',  
        }

        appointment_day = day_map.get(str(data['day']))  

        if appointment_day != current_day:
            raise serializers.ValidationError("You can only book for today in this setup")
        
        return data



class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['id', 'doctor', 'date', 'start_time', 'end_time', 
                 'day_of_week', 'valid_from', 'valid_until', 'available']
        extra_kwargs = {
            'start_time': {'required': True},
            'end_time': {'required': True},
            'date': {'required': True}
        }

    def validate(self, data):
        # Check required fields
        required_fields = ['start_time', 'end_time', 'date']
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError(f"{field} is required")

        # Time validation
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time")

        # Duration validation (max 8 hours)
        delta = datetime.datetime.combine(data['date'], data['end_time']) - \
               datetime.datetime.combine(data['date'], data['start_time'])
        if delta.total_seconds() > 28800:  # 8 hours in seconds
            raise serializers.ValidationError("Maximum slot duration is 8 hours")

        # Date validation
        # if data['date'] < datetime.timezone.now().date():
        if data['date'] < timezone.now().date():

            raise serializers.ValidationError("Cannot create slots for past dates")

        return data