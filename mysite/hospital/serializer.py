from rest_framework import serializers
from .models import *

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['username','first_name','last_name','email',
                  'password','phone_number','profile_picture',
                  'address','date_of_birth']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Patient.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginPatientSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }



class SpecialtySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['specialty']



class DepartmentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['location_name']


class DoctorListSerializer(serializers.ModelSerializer):
    specialty = SpecialtySimpleSerializer()
    departments = DepartmentSimpleSerializer(read_only=True,many=True)
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Doctor
        fields = ['first_name','last_name','specialty','departments',
                  'address','working_days','experience_years','service_price','average_rating']

    def get_average_rating(self,obj):
        return obj.get_average_rating()


class DoctorSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['first_name','last_name',
                  'profile_picture','address','specialty']


class DepartmentsSerializer(serializers.ModelSerializer):
    specialization = SpecialtySimpleSerializer()
    doctor = DoctorListSerializer(many=True)
    class Meta:
        model = Departments
        fields = ['id','specialization','doctor','location_name']



class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name','last_name','role',
                  'phone_number','profile_picture',
                  'date_of_birth','blood_type','ward']


class PatientSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name','last_name','profile_picture','date_of_birth']


class AllergiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergies
        fields = ['allergies','patient']


class AllergiesReadSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer()
    class Meta:
        model = Allergies
        fields = ['allergies','patient']


class AllergiesSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergies
        fields = ['allergies']


class DiagnosisCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['patient','doctor','diagnosis','treatment',]





class AppointmentsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = ['patient_id','doctor_id','time',
                  'date','notes']


class AppointmentsReadListSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format('%H:%M'))
    patient_id = PatientSimpleSerializer(read_only=True)
    doctor_id = DoctorListSerializer()
    class Meta:
        model = Appointments
        fields = ['patient_id','doctor_id','time',
                  'date','notes','status']


class AppointmentsUpdateListSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format('%H:%M'))
    patient_id = PatientSimpleSerializer(read_only=True)

    class Meta:
        model = Appointments
        fields = ['patient_id','doctor_id','time',
                  'date','status']


class AppointmentsSimpleSerializer(serializers.ModelSerializer):
    doctor_id = DoctorSimpleSerializer()
    class Meta:
        model = Appointments
        fields  = ['doctor_id','time','date','status','notes']


class AppointmentsReadDetailSerializer(serializers.ModelSerializer):
    time = serializers.TimeField(format('%H:%M'))
    patient_id = PatientListSerializer()
    doctor_id = DoctorListSerializer()
    class Meta:
        model = Appointments
        fields = ['patient_id','doctor_id','time',
                  'date','notes']

class PrescriptionsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescriptions
        fields = ['medication_name',
                  'dosage','diagnosis']


class PrescriptionsListSerializer(serializers.ModelSerializer):

    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    class Meta:
        model = Prescriptions
        fields = ['medication_name','dosage',
                  'created_at']


class PrescriptionsDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    class Meta:
        model = Prescriptions
        fields = ['medication_name',
                  'dosage','diagnosis','created_at']


class MedicalRecordReadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis',]


class MedicalRecordDetailSerializer(serializers.ModelSerializer):
    patient = PatientListSerializer()
    doctor = DoctorListSerializer()
    date = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    medical = PrescriptionsListSerializer(many=True)
    class Meta:
        model = MedicalRecord
        fields = ['id','patient','doctor','diagnosis',
                  'treatment','date','medical']


class BillingsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billings
        fields = ['patient_id','doctor_id','total_amount','paid']


class BillingsInfoSerializer(serializers.ModelSerializer):
    patient_id = PatientSimpleSerializer()
    class Meta:
        model = Billings
        fields = ['patient_id','total_amount','paid','date']



class WardsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WardsCategory
        fields = ['category']


class WardSerializer(serializers.ModelSerializer):
    ward_category = WardsCategorySerializer
    current_occupancy = serializers.SerializerMethodField(read_only=True)
    patient  = PatientSimpleSerializer()
    class Meta:
        model = Ward
        fields = ['name','ward_category','capacity','current_occupancy','patient']

    def get_current_occupancy(self,obj):
        return obj.get_current_occupancy()


class FeedbacksCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedbacks
        fields = ['docktor_id','patient_id','stars','content',]


class FeedbackReadSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format('%d-%m %H:%M'))
    patient_id = PatientSimpleSerializer()
    class Meta:
        model = Feedbacks
        fields = ['patient_id','content','created_at','stars']



class SpecialtySerializer(serializers.ModelSerializer):
    doctors = DoctorListSerializer(many=True)
    class Meta:
        model = Specialty
        fields = ['specialty','doctors']

class DoctorDetailSerializer(serializers.ModelSerializer):
    doctor_feedback = FeedbackReadSerializer(many=True,read_only=True)
    departments = DepartmentSimpleSerializer(read_only=True,many=True)
    class Meta:
        model = Doctor
        fields = ['first_name','last_name','phone_number',
                  'address','date_of_birth','specialty','shift_start',
                  'shift_end','qualifications','experience_years',
                  'working_days','service_price','departments',
                  'doctor_feedback']

class DoctorDetailFORDoctorSerializer(serializers.ModelSerializer):
    doctor_feedback = FeedbackReadSerializer(many=True,read_only=True)
    departments = DepartmentSimpleSerializer(read_only=True,many=True)
    appointments_doctor = AppointmentsReadListSerializer(read_only=True,many=True)
    billings = BillingsInfoSerializer(many=True)
    class Meta:
        model = Doctor
        fields = ['first_name','last_name','phone_number',
                  'address','date_of_birth','specialty','shift_start',
                  'shift_end','qualifications','experience_years',
                  'working_days','service_price','departments',
                  'doctor_feedback','appointments_doctor','billings']



class PatientDetailSerializer(serializers.ModelSerializer):
    allergies = AllergiesSimpleSerializer(many=True)
    history = MedicalRecordReadListSerializer(many=True)
    billings = BillingsInfoSerializer(many=True)
    ward = WardSerializer()
    date_of_birth = serializers.DateTimeField(format('%d-%m-%Y'))
    appointments_patient = AppointmentsReadListSerializer(read_only=True,many=True)
    class Meta:
        model = Patient
        fields = ['first_name','last_name','profile_picture',
                  'role','phone_number','address',
                  'date_of_birth','emergency_contact',
                  'blood_type','blood_type','allergies',
                  'history','billings','ward','appointments_patient']

class WarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warnings
        fields = ['doctor','patient','ward','created_time']