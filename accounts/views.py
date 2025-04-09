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
    MedicalRecordSerializer, 
    PatientSerializer, 
    AppointmentSerializer, 
    AvailabilitySerializer,
    DoctorSerializer
)
import datetime
from rest_framework import status
from .models import MedicalRecord, Appointment, Availability, Patient, Doctor
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import *
from .serializers import split_into_sessions


User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    """
    A viewset for handling user authentication and registration.
    """ 
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

class AppointmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling appointment-related actions."""
    # permission_classes  = [permissions.IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    

    @action(
            methods=[
                'GET'
            ],
            detail=False
        )
    def available_slots(self, request):
        doctor = request.query_params.get('doctor')
        date = request.query_params.get('date')

        slots = Availability.objects.filter(available=True)
        if doctor:
            slots = slots.filter(doctor=doctor)
        if date:
            slots = slots.filter(date=date)

        data = [{
            "id": slot.id,
            "start_time": slot.start_time,
            "end_time": slot.end_time,
            "date": slot.date,
            "doctor": slot.doctor.id,
            "available":  slot.available,
        } for slot in slots]

        return Response(data)



    @action(
        methods=[
            'POST',
        ],
        detail=False,
    )
    def create_appointment(self, validated_data):
        start_time = validated_data['scheduled_time']
        duration = validated_data['duration']
        availability = validated_data['availability']
        availability.available = False
        availability.save()
        # Calculate end time
        dt_start = datetime.datetime.combine(datetime.date.today(), start_time)
        dt_end = dt_start + datetime.timedelta(minutes=duration)
        validated_data['end_time'] = dt_end.time()

        return super().create(validated_data)

    


class AvailabilityViewset(viewsets.ModelViewSet):
    """
     A viewset for handling availability-related actions.
    """
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
            methods=[
                'GET'
            ], 
            detail=False
        )
    def get_available_slots(self, request):
        doctor = request.query_params.get("doctor")
        date = request.query_params.get("date")

        availability = Availability.objects.all()
        if doctor:
            availability = availability.filter(doctor=doctor)
        if date:
            availability = availability.filter(date=date)

        serializer = self.get_serializer(availability, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling patient-related actions.
    """
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


class DoctorViewSet(viewsets.ModelViewSet):
    """A viewset for handling doctor-related actions."""
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
    
    

class MedicalRecordsViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling medical record-related actions.
    """
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
    




class ScheduleAppointmentView(APIView):
    """
    A view for scheduling an appointment.
    """

    def post(self, request, *args, **kwargs):
        data = request.data
        doctor = data.get('doctor_id')
        scheduled_time = data.get('scheduled_time')  # Expected as a time string (e.g., "14:00:00")
        appointment_date = timezone.now().date()  # assuming booking is for today
        duration = 60  # fixed one-hour session

        # Find the doctor's availability for Now!.
        availability = Availability.objects.filter(
            doctor=doctor,
            date=appointment_date,
            available=True
        ).first()

        if not availability:
            return Response({'error': 'Doctor is not available today.'}, status=status.HTTP_400_BAD_REQUEST)

        # Split availability into one-hour sessions.
        sessions = split_into_sessions(availability)
        requested_session = None
        for session_start, session_end in sessions:
            if str(session_start) == scheduled_time:
                requested_session = (session_start, session_end)
                break

        if not requested_session:
            return Response({'error': 'Requested time does not match any available one-hour session.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check for an overlapping appointment for the same doctor at the same session.
        conflict = Appointment.objects.filter(
            doctor_id=doctor,
            day=availability.date.strftime("%A"),  # or however you map day
            scheduled_time=requested_session[0]
        ).exists()

        if conflict:
            return Response({'error': 'This time slot is already booked.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create the appointment (assumes AppointmentSerializer handles the rest)
        serializer = AppointmentSerializer(data={
            'appointment_id': data.get('appointment_id'),
            'patient_id': data.get('patient_id'),
            'doctor_id': doctor,
            'day': availability.date.strftime("%A"),
            'scheduled_time': requested_session[0],
            'duration': duration,
            'end_time': requested_session[1],
            'status': 'scheduled'
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
