from django.urls import path, include, re_path
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import AuthViewSet, PatientViewSet, AppointmentViewSet, DoctorViewSet, MedicalRecordsViewSet, ScheduleAppointmentView,AvailabilityViewset
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register("", AuthViewSet, basename="auth")
router.register("patients", PatientViewSet, basename="patients")
router.register("appointments", AppointmentViewSet, basename='appointments')
router.register("doctors", DoctorViewSet, basename='doctors')
router.register("med-records", MedicalRecordsViewSet, basename='med-records')
router.register('availability', AvailabilityViewset, basename='availability')

urlpatterns = [
    path("login/", AuthViewSet.as_view({"post": "login"}), name="login"),
    path("logout/", AuthViewSet.as_view({"post": "logout"}), name="logout"),
    path("register/", AuthViewSet.as_view({"post": "register"}), name="register"),
    path("password-change/", AuthViewSet.as_view({"post": "password_change"}), name="password-change"),
    path("profile/", AuthViewSet.as_view({"get": "profile", "put": "profile"}), name="profile"),
    path("patients/", PatientViewSet.as_view({"get": "get_patients", "post": "create_patient"}), name="patient-list"),
    path("appointments/", AppointmentViewSet.as_view({"get": "available_slots", "post": "create"}), name="appointment-list"),
    path("doctors/", DoctorViewSet.as_view({"get": "get_doctors", "post": "create_doctor"}), name="doctors-list"),
    path("med-records/", MedicalRecordsViewSet.as_view({"get": "get_medical_records", "post": "create_medical_records"}), name="med-records"),
    path('availability/', AvailabilityViewset.as_view({"post":"create"}), name='availability'),
    path("", include(router.urls)),
]

# Set up the schema view for Swagger and Redoc
schema_view = get_schema_view(
    openapi.Info(
        title="Doctor Appointment Scheduler API",
        default_version='v1',
        description="API documentation for the Doctor Appointments project. This API allows users to manage doctor appointments, patients, and medical records.",
        terms_of_service="https://#.com",
        contact=openapi.Contact(email="rogendopeter@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Add documentation URLs
urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
