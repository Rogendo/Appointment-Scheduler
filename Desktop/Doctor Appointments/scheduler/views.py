import datetime
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from scheduler.models import MedicalRecord, Appointment, Availability, Patient, Doctor,Session
from .serializers import MedicalRecordSerializer, PatientSerializer, AppointmentSerializer, SessionSerializer,DoctorSerializer
from rest_framework import generics
from pytz import timezone
from datetime import datetime
from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.
def home(request):
    pass


@api_view(['GET','POST'])
def medical_records(request):
    if request.method == 'POST':
        # create new record
        serializer = MedicalRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        # Retrieve all RECORDS
        records = MedicalRecord.objects.all() #.order_by('-timestamp')[:100]
        serializer = MedicalRecordSerializer(records, many=True)
        return Response(serializer.data)
    
class MedicalRecordListView(generics.ListAPIView):
    serializer_class = MedicalRecordSerializer
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['medicalrecord_id', 'patient']

    def get_queryset(self):
        return MedicalRecord.objects.order_by('-timestamp')[:100]

class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    filterset_fields = ['appointment_id', 'doctor_id']

    def get_queryset(self):
        return Appointment.objects.order_by('-timestamp')[:100]
    

class PatientListView(generics.ListAPIView):
    serializer_class = PatientSerializer
    filterset_fields = ['patient_id', 'last_name']

    def get_queryset(self):
        return Patient.objects.order_by('-timestamp')[:100]
    

class DoctorListView(generics.ListAPIView):
    serializer_class = DoctorSerializer
    filterset_fields = ['doctor_id', 'last_name']

    def get_queryset(self):
        return Doctor.objects.order_by('-created_at')[:100]
    


# @api_view(['POST'])
# def ScheduleAppointmentView(request):
#     if request.method == "POST":
        
#         patient_id = int(request.POST.get("patient_id"))
#         doctor_id = int(request.POST.get("doctor_id"))
#         appointment_date = datetime.date(int(request.POST.get("appointment_date_year")), 
#                                          int(request.POST.get("appointment_date_month")), 
#                                          int(request.POST.get("appointment_date_day")))
        
#         # Get the doctor's availability records for the specified date
#         availabilities = Availability.objects.filter(doctor=Doctor(id=doctor_id), date=appointment_date)

        
#         # Check if there are any available time slots
#         available_time_slots = []
#         for availability in availabilities:
#             if not availability.available:
#                 continue
            
#             start_time = datetime.datetime.combine(appointment_date, availability.start_time)
#             end_time = datetime.datetime.combine(appointment_date, availability.end_time)
            
#             available_time_slots.append((start_time, end_time))
        
#         # Create a new session instance
#         if available_time_slots:
#             session_data = {
#                 'patient_id': patient_id,
#                 'doctor_id': doctor_id,
#                 'start_time': start_time,
#                 'end_time': end_time
#             }
#             serializer = SessionSerializer(data=session_data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)  # Pass the serialized data to the Response

#         return Response({'message': 'Invalid request'})

@api_view(['POST'])
class ScheduleAppointmentView(APIView):
    def post(self, request):
        patient_id = int(request.data.get("patient_id"))
        doctor_id = int(request.data.get("doctor_id"))
        appointment_date = datetime.date(int(request.data.get("appointment_date_year")), 
                                         int(request.data.get("appointment_date_month")),                                         
                                         int(request.data.get("appointment_date_day")))
        start_time = datetime.time(int(request.data.get("start_hour")), int(request.data.get("start_minute")))
        end_time = datetime.time(int(request.data.get("end_hour")), int(request.data.get("end_minute")))


        # Validate patient and doctor IDs
        if not (Patient.objects.filter(id=patient_id).exists() and Doctor.objects.filter(id=doctor_id).exists()):
            return Response({'message': 'Invalid patient or doctor ID'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the doctor's available time slots for the specified date
        availabilities = Availability.objects.filter(doctor=Doctor(id=doctor_id), date=appointment_date)

        # Check if there are any available time slots that match the requested appointment time
        available_time_slots = []
        for availability in availabilities:
            if not availability.available or (availability.start_time <= start_time and availability.end_time >= end_time):
                continue
            
            available_time_slots.append((start_time, end_time))
        
        # Create a new appointment instance with the provided patient and doctor IDs, as well as the selected start and end times
        if available_time_slots:
            appointment_data = {
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'start_time': start_time,
                'end_time': end_time,
                'status': 'booked'
            }
            serializer = AppointmentSerializer(data=appointment_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)  # Pass the serialized data to the Response

        return Response({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

class AvailabilityView(APIView):
    def get(self, request, doctor_id, date):
        # Get the doctor's available time slots for the specified date
        availabilities = Availability.objects.filter(doctor=Doctor(id=doctor_id), date=date)
        
        # Return a list of available time slots as strings in the format "HH:MM - HH:MM"
        available_time_slots = []
        for availability in availabilities:
            if not availability.available:
                continue
            
            start_time = datetime.time(availability.start_time.hour, availability.start_time.minute)
            end_time = datetime.time(availability.end_time.hour, availability.end_time.minute)
            
            available_time_slots.append(f"{start_time.strftime('%I:%M')} - {end_time.strftime('%I:%M')}")

        return Response({'available_time_slots': available_time_slots})

class AppointmentView(APIView):
    def get(self, request, doctor_id):
        # Get all appointments for the specified doctor
        appointments = Appointment.objects.filter(doctor=Doctor(id=doctor_id))
        
        # Return a list of appointments as strings in the format "Patient Name - Start Time - End Time"
        appointment_list = []
        for appointment in appointments:
            patient_name = Patient.objects.get(id=appointment.patient_id).first_name + ' ' + Patient.objects.get(id=appointment.patient_id).last_name
            start_time = datetime.time(appointment.start_time.hour, appointment.start_time.minute)
            end_time = datetime.time(appointment.end_time.hour, appointment.end_time.minute)
            
            appointment_list.append(f"{patient_name} - {start_time.strftime('%I:%M')} - {end_time.strftime('%I:%M')}")

        return Response({'appointments': appointment_list})
