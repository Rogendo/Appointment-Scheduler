from django.urls import path, include
# from rest_framework import routers
from . import views 
from scheduler.views import MedicalRecordListView,PatientListView, AppointmentListView, ScheduleAppointmentView,DoctorListView


urlpatterns = [
    path('', views.home, name='home'),
    path('medical-records/', views.medical_records, name='records'),
    path('records/list/', MedicalRecordListView.as_view(), name='medical-records-list'),
    path('appointment/list/', AppointmentListView.as_view(), name='appointments-list'),
    path('patients/list/', PatientListView.as_view(), name='patients-list'),
    path('doctors/list/', DoctorListView.as_view(), name='doctors-list'),
    path('schedule-appointment/',views.ScheduleAppointmentView, name = 'schedule'),

]


