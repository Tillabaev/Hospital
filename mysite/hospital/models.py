from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField


class WardsCategory(models.Model):
    category = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.category}'


class Ward(models.Model):
    name = models.CharField(max_length=35)
    ward_category = models.ForeignKey(WardsCategory, on_delete=models.CASCADE)
    capacity =  models.PositiveIntegerField()
    ward_description = models.TextField(null=True,blank=True)
    # capacity_occupancy
    def __str__(self):
        return f'{self.name} - {self.capacity}'

    def get_current_occupancy(self):
        # Получаем всех пациентов, связанных с текущим отделением
        patients_count = self.patient.count()
        return self.capacity - patients_count


WORKING_DAYS = (
    ('Mon','Mon'),
    ('Tue','Tue'),
    ('Wed','Wed'),
    ('Thu','Thu'),
    ('Fri','Fri'),
    ('Sat','Sat'),
    ('Sun','Sun'),
)
class UserProfile(AbstractUser):
    USER_ROLE = (
        ('doctor','doctor'),
        ('patient','patient')
    )
    role = models.CharField(max_length=15,choices=USER_ROLE)
    phone_number = PhoneNumberField(region='KG')
    profile_picture = models.ImageField(upload_to='profile_img/',null=True,blank=True)
    address = models.CharField(max_length=50,null=True,blank=True)
    date_of_birth = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f'{self.first_name} - {self.role}'


class Specialty(models.Model):
    specialty = models.CharField(max_length=55,unique=True)

    def __str__(self):
        return f'{self.specialty}'


class Doctor(UserProfile):
    specialty = models.ForeignKey(Specialty,on_delete=models.CASCADE,related_name='doctors',null=True,blank=True)
    shift_start = models.TimeField(null=True,blank=True)
    shift_end = models.TimeField(null=True,blank=True)
    qualifications = models.CharField(max_length=100)
    experience_years = models.PositiveSmallIntegerField()
    WORKING_DAYS=(
        ('Mon', 'Mon'),
        ('Tue', 'Tue'),
        ('Wed', 'Wed'),
        ('Thu', 'Thu'),
        ('Fri', 'Fri'),
        ('Sat', 'Sat'),
        ('Sun', 'Sun'),
    )
    working_days = MultiSelectField(choices=WORKING_DAYS)
    service_price = models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
        return f'{self.first_name} - {self.specialty}'


    def get_average_rating(self):
        ratings = self.doctor_feedback.all()
        if ratings.exists():
            return (round(sum(rating.stars for rating in ratings) / ratings.count(), 1))
        return 0




class Departments(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='departments')
    specialization = models.ForeignKey(Specialty,on_delete=models.CASCADE)
    location_name = models.CharField(max_length=25)#????

    def __str__(self):
        return f'{self.doctor} - {self.location_name}'


class Patient(UserProfile):
    emergency_contact = models.CharField(max_length=100)
    BLOOD_TYPE = (
        ('O+','O+'),
        ('O-','O-'),
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-')
    )
    blood_type = models.CharField(max_length=10,choices=BLOOD_TYPE)
    ward = models.ForeignKey(Ward,on_delete=models.CASCADE,related_name='patient',null=True,blank=True)

    def __str__(self):
        return f'{self.first_name} - {self.blood_type} '

class Allergies(models.Model):
    allergies = models.CharField(max_length=25)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='allergies')

    def __str__(self):
        return f'{self.allergies} - {self.patient}'


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='history')
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    diagnosis  = models.TextField(null=True,blank=True)
    treatment = models.TextField(null=True,blank=True)

    def __str__(self):
        return f'{self.patient} - {self.diagnosis} '


class Appointments(models.Model):
    patient_id = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='appointments_patient')
    doctor_id = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='appointments_doctor')
    time = models.TimeField()
    date = models.CharField('Doctor',max_length=25,choices=Doctor.WORKING_DAYS)#????
    STATUS = (
        ('wait','wait'),
        ('recorded','recorded'),
        ('refused','refused'),
    )
    status = models.CharField(max_length=25,choices=STATUS,default='wait')
    notes = models.TextField(null=True,blank=True)


    def __str__(self):
        return f'{self.patient_id} - {self.status}  - {self.doctor_id}'



class Prescriptions(models.Model):
    medication_name = models.CharField(max_length=55)
    dosage = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    diagnosis = models.ForeignKey(MedicalRecord,on_delete=models.CASCADE,related_name='medical')


    def __str__(self):
        return f'{self.dosage} - {self.medication_name}'


class Billings(models.Model):
    patient_id = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='billings')
    total_amount = models.PositiveIntegerField()
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    doctor_id = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='billings')


    def __str__(self):
        return f'{self.patient_id} - {self.total_amount} - {self.paid}'




class Feedbacks(models.Model):
    docktor_id = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='doctor_feedback')
    patient_id = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='patient_feedback')
    content = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    stars = models.PositiveSmallIntegerField(choices=[(i,str(i)) for i in range(6)])#charfield


    def __str__(self):
        return f'{self.patient_id} - {self.docktor_id} - {self.stars}'


class Warnings(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward,on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateTimeField(auto_now_add=True)



class Message(models.Model):
    author = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    text = models.TextField(null=True,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='message_img/',null=True,blank=True)
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE)
    video = models.FileField(upload_to='message_video',null=True,blank=True)

