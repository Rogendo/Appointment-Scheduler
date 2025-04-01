from django.db import models
# from autoslug import AutoSlugField
import datetime
# Create your models here.


class Doctor(models.Model):
    AVAILABILITY_STATUS = [
        ("available","Available"),
        ("occupied","Occupied"),
        
    ]

    doctor_id = models.IntegerField(8)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    # slug = AutoSlugField(unique_with="id", populate_from="last_name")

    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_STATUS, default='availabe')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




    class Meta:
        verbose_name_plural = 'Doctors'
        ordering = ['last_name']

        def __str__(self):
            return self.name
        

class Patient(models.Model):
    patient_id = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10)
    email = models.CharField(max_length=100, null=True)
    date_of_birth = models.DateTimeField()
    # insurance_details = models.FileField(null=True)
    insurance_number = models.CharField(max_length=100)
    insurance_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Patients'
        ordering = ['last_name']

        def __str__(self):
            return self.name
        
class Appointment(models.Model):
    STATUS = [
    ("booked","Booked"),
    ("not booked","Not Booked"),
    ]

    appointment_id = models.IntegerField()
    patient_id = models.ForeignKey(Patient, verbose_name=("patients"), on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, verbose_name=("doctor"), on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS)

    # created_on = models.DateTimeField(auto_now_add=True)


    # scheduled_time = models.DateTimeField(auto_now_add=True)

    # end_time =                 # calculated as scheduled_time + duration


class Availability(models.Model):
    
    doctor =  models.ForeignKey(Doctor, verbose_name=("doctor"), on_delete=models.CASCADE)
    date = models.DateTimeField()
    start_time =  models.DateTimeField(auto_now_add=True)
    end_time =  models.DateTimeField(auto_now_add=True)
    available = models.BooleanField()

    class Meta:
        verbose_name_plural = 'Availability'
        # ordering = ['last_name']

        def __str__(self):
            return self.doctor
     
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
    medicalrecord_id = models.IntegerField()
    patient = models.ForeignKey(Patient, verbose_name=("patients"), on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, verbose_name=("doctor"), on_delete=models.CASCADE)
    record_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.CharField(max_length=10000)
    prescription = models.CharField(max_length=1000)
    notes = models.CharField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)

