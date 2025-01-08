from django.urls import path,include

from .views import *



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-student_list'),
    path('login/', CustomLoginView.as_view(), name='login-student_list'),
    path('logout/', LogoutViewPatient.as_view(), name='logout-student_list'),

    path('specialty/',SpecialtyListAPIView.as_view(),name = 'doctor-specialty'),

    path('record/create/',DiagnosisCreateAPIView.as_view(),name = 'diagnosis-create'),
    path('record/', DiagnosisReadListAPIView.as_view(), name='diagnosis_list'),
    path('record/<int:pk>/', DiagnosisReadDetailAPIView.as_view(), name='diagnosis'),

    path('appointments/',AppointmentsListAPIView.as_view(),name = 'appointments_list'),
    path('appointments/<int:pk>/',AppointmentsDetailAPIView.as_view(),name = 'appointments_detail'),
    path('appointments/create/',AppointmentsCreateAPIView.as_view(),name = 'appointments_create'),

    path('appointments/update/<int:pk>/',AppointmentsUPDATEAPIView.as_view(),name = 'appointments_updated'),

    path('prescriptions/',PrescriptionsListAPIView.as_view(),name = 'prescriptions_list'),
    path('prescriptions/<int:pk>/',PrescriptionsDetailAPIView.as_view(),name = 'prescriptions_detail'),
    path('prescriptions/create/',PrescriptionsCreateAPIView.as_view(),name = 'prescriptions_create'),

    path('allergies/',AllergiesCreateAPIView.as_view(),name = 'allergies_create'),


    path('feedbacks/create/',FeedbacksCreateAPIView.as_view(),name = 'feedbacks_create'),
    path('feedback/<int:pk>/',FeedbackDeleteAPIView.as_view(),name = 'feedback_detail'),

    path('ward/',WardListAPIView.as_view(),name = 'ward_list'),
    path('ward/category/',WardCategoryListAPIView.as_view(),name = 'ward_category'),


    path('billing/create/',BillingsCreateAPIView.as_view(),name = 'billing_create'),
    path('billing/list/',BillingsListAPIView.as_view(),name = 'billing_list'),


    path('doctor/',DoctorListAPIView.as_view(),name = 'doctor_profile'),
    path('doctor/<int:pk>/',DoctorDetailAPIView.as_view(),name = 'doctor_detail'),
    path('doctorr/<int:pk>/',DoctorProfileDetail.as_view(),name = 'doctor_'),


    path('patient/list/',PatientListAPIView.as_view(),name = 'patient_list'),
    path('patient/', PatientDetailAPIView.as_view(), name='patient'),

    path('warnings/create/',WarningsCreateAPIView.as_view(),name = 'warning')
]
