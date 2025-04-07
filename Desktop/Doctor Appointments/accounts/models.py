from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.utils import UserManager


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

    doctor_id = models.IntegerField(unique=True, primary_key=True)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    department = models.CharField(max_length=40, choices=DEPARTMENT)
    phone_no = models.CharField(max_length=10,unique=True)
    # email = models.CharField(max_length=100,unique=True)
    # slug = AutoSlugField(unique_with="id", populate_from="last_name")
    user_type = CustomUser.user_type
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
        return str(self.timestamp)    


class Availability(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()  
    start_time = models.TimeField()  
    end_time = models.TimeField()  
    day_of_week = models.CharField(max_length=20, choices=DAY_CHOICES)
    valid_from = models.DateField()
    valid_until = models.DateField()
    available = models.BooleanField(default=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.doctor} - {self.date} {self.start_time}-{self.end_time}"
     
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

    