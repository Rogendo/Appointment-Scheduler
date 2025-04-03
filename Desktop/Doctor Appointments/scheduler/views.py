import datetime
from xml.dom import ValidationErr
from django.shortcuts import render
from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from scheduler.models import MedicalRecord, Appointment, Availability, Patient, Doctor,Session
from .serializers import MedicalRecordSerializer, PatientSerializer, AppointmentSerializer, AvailabilitySerializer,DoctorSerializer
from rest_framework import generics
from pytz import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from rest_framework.views import APIView

# # Create your views here.
# def home(request):
#     pass

    


# # @api_view(['POST'])
# # def ScheduleAppointmentView(request):
# #     if request.method == "POST":
        
# #         patient_id = int(request.POST.get("patient_id"))
# #         doctor_id = int(request.POST.get("doctor_id"))
# #         appointment_date = datetime.date(int(request.POST.get("appointment_date_year")), 
# #                                          int(request.POST.get("appointment_date_month")), 
# #                                          int(request.POST.get("appointment_date_day")))
        
# #         # Get the doctor's availability records for the specified date
# #         availabilities = Availability.objects.filter(doctor=Doctor(id=doctor_id), date=appointment_date)

        
# #         # Check if there are any available time slots
# #         available_time_slots = []
# #         for availability in availabilities:
# #             if not availability.available:
# #                 continue
            
# #             start_time = datetime.datetime.combine(appointment_date, availability.start_time)
# #             end_time = datetime.datetime.combine(appointment_date, availability.end_time)
            
# #             available_time_slots.append((start_time, end_time))
        
# #         # Create a new session instance
# #         if available_time_slots:
# #             session_data = {
# #                 'patient_id': patient_id,
# #                 'doctor_id': doctor_id,
# #                 'start_time': start_time,
# #                 'end_time': end_time
# #             }
# #             serializer = SessionSerializer(data=session_data)
# #             if serializer.is_valid():
# #                 serializer.save()
# #                 return Response(serializer.data)  # Pass the serialized data to the Response

# #         return Response({'message': 'Invalid request'})

# @api_view(['POST'])
# class ScheduleAppointmentView(APIView):
#     def post(self, request):
#         serializer = AppointmentSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         data = serializer.validated_data
#         doctor = data['doctor']
#         date = data['date']
#         start = data['start_time']
#         end = data['end_time']

#         # 1. Check doctor availability
#         available_slots = Availability.objects.filter(
#             doctor=doctor,
#             date=date,
#             start_time__lte=start,
#             end_time__gte=end,
#             available=True
#         ).exists()

#         if not available_slots:
#             return Response({'error': 'Doctor not available at this time'}, 
#                           status=status.HTTP_400_BAD_REQUEST)

#         # 2. Check existing appointments
#         conflicting_appointments = Appointment.objects.filter(
#             doctor=doctor,
#             date=date,
#             status='booked'
#         ).filter(
#             models.Q(start_time__lt=end, end_time__gt=start)
#         ).exists()

#         if conflicting_appointments:
#             return Response({'error': 'Time slot already booked'}, 
#                           status=status.HTTP_409_CONFLICT)

#         # 3. Create appointment
#         appointment = serializer.save()
        
#         # 4. Optional: Mark availability slot as taken
#         Availability.objects.filter(
#             doctor=doctor,
#             date=date,
#             start_time__lte=start,
#             end_time__gte=end
#         ).update(available=False)

#         return Response(AppointmentSerializer(appointment).data, 
#                       status=status.HTTP_201_CREATED)
    

# class AvailabilityView(APIView):
#     def get(self, request, doctor_id):
#         date_str = request.query_params.get('date')
#         try:
#             date = datetime.strptime(date_str, '%Y-%m-%d').date()
#         except (ValueError, TypeError):
#             return Response({'error': 'Invalid date format. Use YYYY-MM-DD'}, 
#                           status=status.HTTP_400_BAD_REQUEST)

#         availabilities = Availability.objects.filter(
#             doctor_id=doctor_id,
#             date=date
#         )
#         serializer = AvailabilitySerializer(availabilities, many=True)
#         return Response(serializer.data)

# class DoctorAppointmentsView(generics.ListAPIView):
#     serializer_class = AppointmentSerializer
    
#     def get_queryset(self):
#         doctor_id = self.kwargs['doctor_id']
#         return Appointment.objects.filter(
#             doctor_id=doctor_id,
#             status='booked'
#         ).order_by('date', 'start_time')
# # class AvailabilityView(APIView):
# #     def get(self, request, doctor_id, date):
# #         # Get the doctor's available time slots for the specified date
# #         availabilities = Availability.objects.filter(doctor=Doctor(id=doctor_id), date=date)
        
# #         # Return a list of available time slots as strings in the format "HH:MM - HH:MM"
# #         available_time_slots = []
# #         for availability in availabilities:
# #             if not availability.available:
# #                 continue
            
# #             start_time = datetime.time(availability.start_time.hour, availability.start_time.minute)
# #             end_time = datetime.time(availability.end_time.hour, availability.end_time.minute)
            
# #             available_time_slots.append(f"{start_time.strftime('%I:%M')} - {end_time.strftime('%I:%M')}")

# #         return Response({'available_time_slots': available_time_slots})

# # class AppointmentView(APIView):
# #     def get(self, request, doctor_id):
# #         # Get all appointments for the specified doctor
# #         appointments = Appointment.objects.filter(doctor=Doctor(id=doctor_id))
        
# #         # Return a list of appointments as strings in the format "Patient Name - Start Time - End Time"
# #         appointment_list = []
# #         for appointment in appointments:
# #             patient_name = Patient.objects.get(id=appointment.patient_id).first_name + ' ' + Patient.objects.get(id=appointment.patient_id).last_name
# #             start_time = datetime.time(appointment.start_time.hour, appointment.start_time.minute)
# #             end_time = datetime.time(appointment.end_time.hour, appointment.end_time.minute)
            
# #             appointment_list.append(f"{patient_name} - {start_time.strftime('%I:%M')} - {end_time.strftime('%I:%M')}")

# #         return Response({'appointments': appointment_list})

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






class PatientViewSet(viewsets.ModelViewSet):
    permission_classes  = [permissions.IsAuthenticated]
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