from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from accounts.utils import get_and_authenticate_user, create_user_account
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, logout
from .serializers import (
    EmptySerializer,
    UserLoginSerializer,
    AuthUserSerializer,
    UserRegisterSerializer,
    PasswordChangeSerializer,
    AccountProfileSerializer,
)


User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [
        AllowAny,
    ]
    serializer_class = EmptySerializer
    serializer_classes = {
        "login": UserLoginSerializer,
        "register": UserRegisterSerializer,
        "password_change": PasswordChangeSerializer,
        "profile": AccountProfileSerializer,
    }

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def profile(self, request):
        if request.method == "GET":
            profile = User.objects.get(email=request.user.email)
            serializer = self.get_serializer(profile)
            data = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            profile = User.objects.get(email=request.user.email)
            serializer = self.get_serializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def logout(self, request):
        logout(request)
        data = {"success": "Successfully logged out"}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response(status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
import datetime
from xml.dom import ValidationErr
from django.shortcuts import render
from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import MedicalRecord, Appointment, Availability, Patient, Doctor
from rest_framework import generics
from pytz import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from .serializers import (MedicalRecordSerializer, 
                          PatientSerializer, 
                          AppointmentSerializer, 
                          AvailabilitySerializer,
                          DoctorSerializer)
from .models import *
class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes  = [permissions.IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    @action(
        methods=[
            'GET',
        ],
        detail=False,
    )
    def get_appointments(self,request):
        appointments = Appointment.objects.all()
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(
        methods=[
            'POST',
        ],
        detail=False,
    )
    def create_appointment(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    @action(
        methods=[
        'PUT'
    ],
    detail=False,
    )

    def update_appointment(self, request):
        appointment = Appointment.objects.get(id=request.data.get('appointment_id'))
        serializer = self.get_serializer(appointment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(
        methods=[
            "DELETE",
        ],
        detail=False,
    )
    def delete_appointment(self, request):
        appointment = Appointment.objects.get(id=request.data.get("appointment_id"))
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AvailabilityViewset(viewsets.ModelViewSet):
    # permission_classes  = [permissions.IsAuthenticated]
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    @action(
        methods=[
            'GET',
        ],
        detail=False,
    )

    def get_available_slots(self,request):
        availability = Availability.objects.all()
        serializer = self.get_serializer(availability, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(
        methods=[
            'POST',
        ],
        detail=False,
    )
    def create_availability_slot(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    @action(
        methods=[
        'PUT'
    ],
    detail=False,
    )

    def update_availability_slot(self, request):
        availability = Availability.objects.get(id=request.data.get('doctor_id'))
        serializer = self.get_serializer(availability, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(
        methods=[
            "DELETE",
        ],
        detail=False,
    )
    def delete_availability_slot(self, request):
        availability = Patient.objects.get(id=request.data.get("doctor_id"))
        availability.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class PatientViewSet(viewsets.ModelViewSet):
    # permission_classes  = [permissions.IsAuthenticated]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    @action(
        methods=[
            'GET',
        ],
        detail=False,
    )

    def get_patients(self,request):
        patients = Patient.objects.all()
        serializer = self.get_serializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(
        methods=[
            'POST',
        ],
        detail=False,
    )
    def create_patient(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    @action(
        methods=[
        'PUT'
    ],
    detail=False,
    )

    def update_patient(self, request):
        patient = Patient.objects.get(id=request.data.get('patient_id'))
        serializer = self.get_serializer(patient, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(
        methods=[
            "DELETE",
        ],
        detail=False,
    )
    def delete_patient(self, request):
        patient = Patient.objects.get(id=request.data.get("patient_id"))
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorViewSet(viewsets.ModelViewSet):
    permission_classes  = [permissions.IsAuthenticated]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    @action(
        methods=[
            'GET',
        ],
        detail=False,
    )

    def get_doctors(self,request):
        doctors = Doctor.objects.all()
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(
        methods=[
            'POST',
        ],
        detail=False,
    )
    def create_doctor(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    @action(
        methods=[
        'PUT'
    ],
    detail=False,
    )

    def update_doctor(self, request):
        doctor = Doctor.objects.get(id=request.data.get('doctor_id'))
        serializer = self.get_serializer(doctor, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(
        methods=[
            "DELETE",
        ],
        detail=False,
    )
    def delete_doctor(self, request):
        doctor = Doctor.objects.get(id=request.data.get("doctor_id"))
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MedicalRecordsViewSet(viewsets.ModelViewSet):
    permission_classes  = [permissions.IsAuthenticated]
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    @action(
        methods=[
            'GET',
        ],
        detail=False,
    )

    def get_medical_records(self,request):
        medical_records = MedicalRecord.objects.all()
        serializer = self.get_serializer(medical_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(
        methods=[
            'POST',
        ],
        detail=False,
    )
    def create_medical_records(self,request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

    @action(
        methods=[
        'PUT'
    ],
    detail=False,
    )

    def update_medical_record(self, request):
        medical_record = MedicalRecord.objects.get(id=request.data.get('medicalrecords_id'))
        serializer = self.get_serializer(medical_record, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @action(
        methods=[
            "DELETE",
        ],
        detail=False,
    )
    def delete_medical_record(self, request):
        medical_record = MedicalRecord.objects.get(id=request.data.get("medicalrecords_id"))
        medical_record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


# class AppointmentCreateView(generics.CreateAPIView):
#     serializer_class = AppointmentSerializer
#     required_scopes = ['write']

#     def perform_create(self, serializer):
#         # Add conflict checking logic
#         if self._has_conflict(serializer.validated_data):
#             raise ValidationErr("Time slot unavailable")
#         serializer.save()

#     def _has_conflict(self, data):
#         return Appointment.objects.filter(
#             doctor=data['doctor'],
#             date_time__range=(
#                 data['date_time'] - timedelta(minutes=29),
#                 data['date_time'] + timedelta(minutes=29)
#             )
#         ).exists()


@api_view(['POST'])
class ScheduleAppointmentView(APIView):
    def __init__(self, *args, **kwargs):
        super(ScheduleAppointmentView)  
        super().__init__(*args, **kwargs)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        doctor = data['doctor']
        date = data['date']
        start = data['start_time']
        end = data['end_time']

        # 1. Check doctor availability
        available_slots = Availability.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lte=start,
            end_time__gte=end,
            available=True
        ).exists()

        if not available_slots:
            return Response({'error': 'Doctor not available at this time'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # 2. Check existing appointments
        conflicting_appointments = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            status='booked'
        ).filter(
            models.Q(start_time__lt=end, end_time__gt=start)
        ).exists()

        if conflicting_appointments:
            return Response({'error': 'Time slot already booked'}, 
                          status=status.HTTP_409_CONFLICT)

        # 3. Create appointment
        appointment = serializer.save()
        
        # 4. Optional: Mark availability slot as taken
        Availability.objects.filter(
            doctor=doctor,
            date=date,
            start_time__lte=start,
            end_time__gte=end
        ).update(available=False)

        return Response(AppointmentSerializer(appointment).data, 
                      status=status.HTTP_201_CREATED)