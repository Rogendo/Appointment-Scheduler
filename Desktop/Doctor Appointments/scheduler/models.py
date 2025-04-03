from django.db import models
# from autoslug import AutoSlugField
import datetime
# Create your models here.
from accounts.models import CustomUser

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

    doctor_id = models.IntegerField(unique=True, primary_key=True)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    department = models.CharField(max_length=40, choices=DEPARTMENT)
    phone_no = models.CharField(max_length=10,unique=True)
    # email = models.CharField(max_length=100,unique=True)
    # slug = AutoSlugField(unique_with="id", populate_from="last_name")

    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='availabe')
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)




    class Meta:
        verbose_name_plural = 'Doctors'
        ordering = ['last_name']

    def __str__(self):
        return self.last_name
    

class Patient(models.Model):
    patient_id = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10, unique=True)
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


class Appointment(models.Model):
    STATUS = [
    ("scheduled","Scheduled"),
    ("canceled","Canceled"),
    ("completed","Completed"),
    ]
    DAY = [
            ('1','Monday'),
            ('2','Teusday'),
            ('3','Wednesday'),
            ('4','Thurday'),
            ('5','Friday'),
        ]

    appointment_id = models.IntegerField(unique=True,primary_key=True)
    patient_id = models.ForeignKey(Patient, verbose_name=("patients"), on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, verbose_name=("doctor"), on_delete=models.CASCADE)   
    # day = models.DateField(verbose_name='day')    
    day =  models.CharField(max_length=20, choices=DAY)
    scheduled_time = models.TimeField()
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(verbose_name='duration (min)')
    status = models.CharField(max_length=20, choices=STATUS)
    end_time = models.TimeField() # datetime.timedelta.min(start_time) + duration # Compute the endtime # - end_time (datetime)  # could be calculated based on duration, but maybe store it
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    # end_time =                 # calculated as scheduled_time + duration
    class Meta:
        verbose_name_plural = 'Appointments'
        ordering = ['timestamp']

    def __str__(self):
        return self.appointment_id    

class Availability(models.Model):
    av_id = models.IntegerField(unique=True, primary_key=True)
    doctor =  models.ForeignKey(Doctor, verbose_name=("doctor"), on_delete=models.CASCADE)
    date = models.DateTimeField()
    start_time =  models.DateTimeField(auto_now_add=True)
    end_time =  models.DateTimeField(auto_now_add=True)
    DAY = [
        ('1','Monday'),
        ('2','Teusday'),
        ('3','Wednesday'),
        ('4','Thurday'),
        ('5','Friday'),
    ]
    day_of_week = models.CharField(max_length=20, choices=DAY)
    valid_from = models.DateField()
    valid_until = models.DateField()
    available = models.BooleanField()


    def __str__(self):
        return self.doctor
    class Meta:
        verbose_name_plural = 'Availability'
        # ordering = ['last_name']

 
     
# class Session(models.Model):
#     patient = models.ForeignKey(Patient, verbose_name=("patients"), on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, verbose_name=("patients"), on_delete=models.CASCADE)
#     start_time =  models.DateTimeField(auto_now_add=True)
#     end_time =  models.DateTimeField(auto_now_add=True)
   
class Session(models.Model):
    patient_id = models.IntegerField()
    doctor_id = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class MedicalRecord(models.Model):
    medicalrecord_id = models.IntegerField(unique=True)
    patient = models.ForeignKey(Patient, verbose_name=("patient"), on_delete=models.CASCADE)
    # appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, verbose_name=("doctors"), on_delete=models.CASCADE)
    record_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.CharField(max_length=10000)
    prescription = models.CharField(max_length=1000)
    notes = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.medicalrecord_id
    class Meta:
        verbose_name_plural = 'MedicalRecords'
        # ordering = ['patient']

    