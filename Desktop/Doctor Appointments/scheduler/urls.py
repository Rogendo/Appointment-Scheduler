from django.urls import path, include
from rest_framework import routers
from . import views 
from scheduler.views import (
    # MedicalRecordListView,
                            #  PatientListView,AvailabilityView, 
                            #  DoctorAppointmentsView, 
                            #  AppointmentListView, 
                             ScheduleAppointmentView,
                            #  DoctorListView,
                             PatientViewSet,
                             AppointmentViewSet,
                             DoctorViewSet,
                             MedicalRecordsViewSet,
                            #  AppointmentCreateView
                             )


router = routers.DefaultRouter(trailing_slash=False)

router.register("patients", PatientViewSet, basename="patients")
router.register("appointments", AppointmentViewSet, basename='appointments')
router.register("doctors", DoctorViewSet, basename='doctors')
router.register("med-records", MedicalRecordsViewSet, basename='med-records')
# router.register("schedule", AppointmentCreateView, basename='schedule')

urlpatterns = [
    path(
        "patients/",
        PatientViewSet.as_view({"get": "get_patients", "post": "create_patient"}),
        name="patient-list",
    ),
    path(
        "appointments/",
        AppointmentViewSet.as_view({"get": "get_appointments", "post": "create_appointment"}),
        name="appointment-list",
    ),

    path(
        "doctors/",
        DoctorViewSet.as_view({"get": "get_doctors", "post": "create_doctor"}),
        name="doctors-list",
    ),
    path(
        "med-records/",
        MedicalRecordsViewSet.as_view({"get": "get_medical_records", "post": "create_medical_records"}),
        name="med-records",
    ),

    # path(
    #     "schedule/",
    #     AppointmentCreateView,
    #     name="schedule",
    # ),

    path("", include(router.urls)),
    path('schedule-appointment/',views.ScheduleAppointmentView, name = 'schedule'),


]


# urlpatterns = [
#     path('', views.home, name='home'),
#     path('medical-records/', views.medical_records, name='records'),
#     path('records/list/', MedicalRecordListView.as_view(), name='medical-records-list'),
#     path('appointment/list/', AppointmentListView.as_view(), name='appointments-list'),
#     path('patients/list/', PatientListView.as_view(), name='patients-list'),
#     path('doctors/list/', DoctorListView.as_view(), name='doctors-list'),
#     path('schedule-appointment/',views.ScheduleAppointmentView, name = 'schedule'),
#     path('availability/<int:doctor_id>/', AvailabilityView.as_view(), name='doctor-availability'),
#     path('appointments/<int:doctor_id>/', DoctorAppointmentsView.as_view(), name='doctor-appointments'),
# ]


