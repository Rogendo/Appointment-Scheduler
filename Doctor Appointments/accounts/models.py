from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.utils import UserManager
from datetime import datetime, timedelta

class CustomUser(AbstractUser):
    TYPE_CHOICES = (("", "Select"), ("doctor", "doctor"), ("user", "user"))
    username = None
    email = models.EmailField(("email address"), unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    bio = models.TextField()
    phone_number = models.CharField(max_length=10, default="07XXXXXXXX")
    user_type = models.CharField(max_length=90, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "users"


class Doctor(CustomUser):
    AVAILABILITY_STATUS = [
        ("available","Available"),
        ("occupied","Occupied"),   
    ]
    DEPARTMENT = [
        ('paedetrics','Paedetrics'),
        ('optics', 'Optics'),
        ('oncology','Oncology'),
        ('dentist','Dentist'),
        ('hiv/aids','HIV/AIDS'),
        ('maternity','Maternity')

    ]

    doctor_id = models.AutoField(primary_key=True)
    specialization = models.CharField(max_length=200)
    department = models.CharField(max_length=40, choices=DEPARTMENT)
    user_type = CustomUser.user_type
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='available')
    

    def __str__(self):
        return self.last_name
    

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10, unique=True,default="07XXXXXXXX")
    email = models.CharField(max_length=100, unique=True,null=True)
    date_of_birth = models.DateTimeField()
    # insurance_details = models.FileField(null=True)
    insurance_number = models.CharField(max_length=100)
    insurance_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Patients'
        ordering = ['last_name']

    def __str__(self):
        return self.last_name

class Availability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('doctor', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.doctor} | {self.date} {self.start_time}-{self.end_time} | {'Available' if self.available else 'Booked'}"
    
    def save(self, *args, **kwargs):
        # Prevent saving parent slot - only save children
        if not self.pk:
            slots = []
            current_start = self.start_time

            while current_start < self.end_time:
                current_end = (datetime.combine(self.date, current_start) + timedelta(hours=1))
                if current_end.time() > self.end_time:
                    current_end = datetime.combine(self.date, self.end_time)

                # Check if the slot already exists
                if not Availability.objects.filter(
                    doctor=self.doctor,
                    date=self.date,
                    start_time=current_start,
                    end_time=current_end.time()
                ).exists():
                    slots.append(Availability(
                        doctor=self.doctor,
                        date=self.date,
                        start_time=current_start,
                        end_time=current_end.time(),
                        available=self.available
                    ))
                current_start = current_end.time()

            # Bulk create only non-duplicate slots
            if slots:
                Availability.objects.bulk_create(slots)
            return  # Skip saving original instance
        super().save(*args, **kwargs)


class Appointment(models.Model):
    STATUS = [
        ("scheduled", "Scheduled"),
        ("canceled", "Canceled"),
        ("completed", "Completed"),
    ]

    appointment_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    scheduled_time = models.TimeField()
    duration = models.PositiveIntegerField(verbose_name='Duration (minutes)')
    end_time = models.TimeField(editable=False)
    status = models.CharField(max_length=20, choices=STATUS, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        ordering = ['date', 'scheduled_time']
        unique_together = ('doctor', 'date', 'scheduled_time', 'end_time')

    def save(self, *args, **kwargs):
        # Calculate end_time
        start = datetime.combine(self.date, self.scheduled_time)
        self.end_time = (start + timedelta(minutes=self.duration)).time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} {self.scheduled_time} - {self.doctor}"
    


class MedicalRecord(models.Model):
    medicalrecord_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    record_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.CharField(max_length=10000)
    prescription = models.CharField(max_length=1000)
    notes = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.appointment)
    
    class Meta:
        verbose_name_plural = 'MedicalRecords'
        ordering = ['appointment']
        unique_together = ('appointment',) 

    