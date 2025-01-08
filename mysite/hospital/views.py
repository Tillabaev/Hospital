from rest_framework import viewsets,generics,status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .serializer import *
from .filters import *

from .pagination import *
from .permission import *

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    serializer_class =PatientSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginPatientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutViewPatient(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class SpecialtyListAPIView(generics.ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer




class PatientListAPIView(generics.ListAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer
    pagination_class = PatientPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blood_type']


class AllergiesCreateAPIView(generics.ListAPIView):
    queryset = Allergies.objects.all()
    serializer_class = AllergiesSerializer




class DiagnosisCreateAPIView(generics.CreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = DiagnosisCreateSerializer
    permission_classes = [CheckDoctorTrue]


class DiagnosisReadListAPIView(generics.ListAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordReadListSerializer


class DiagnosisReadDetailAPIView(generics.RetrieveAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordDetailSerializer


class AppointmentsCreateAPIView(generics.CreateAPIView):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentsCreateSerializer
    permission_classes = [permissions.IsAuthenticated,CheckDoctorFalse]

class AppointmentsListAPIView(generics.ListAPIView):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentsReadListSerializer


class AppointmentsDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentsReadDetailSerializer

class AppointmentsUPDATEAPIView(generics.RetrieveUpdateAPIView):
    queryset = Appointments.objects.all()
    serializer_class = AppointmentsUpdateListSerializer
    permission_classes = [CheckDoctorTrue]


class PrescriptionsCreateAPIView(generics.CreateAPIView):
    queryset = Prescriptions.objects.all()
    serializer_class = PrescriptionsCreateSerializer
    permission_classes = [CheckDoctorTrue]

class PrescriptionsListAPIView(generics.ListAPIView):
    queryset = Prescriptions.objects.all()
    serializer_class = PrescriptionsListSerializer

class PrescriptionsDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Prescriptions.objects.all()
    serializer_class = PrescriptionsDetailSerializer


class BillingsCreateAPIView(generics.CreateAPIView):
    queryset = Billings.objects.all()
    serializer_class = BillingsCreateSerializer
    permission_classes = [CheckDoctorTrue]

class BillingsListAPIView(generics.ListAPIView):
    queryset = Billings.objects.all()
    serializer_class = BillingsInfoSerializer

class WardCategoryListAPIView(generics.ListAPIView):
    queryset = WardsCategory.objects.all()
    serializer_class = WardsCategorySerializer


class WardListAPIView(generics.ListAPIView):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer

class FeedbacksCreateAPIView(generics.CreateAPIView):
    serializer_class = FeedbacksCreateSerializer
    permission_classes = [permissions.IsAuthenticated,CheckDoctorFalse]


class FeedbackDeleteAPIView(generics.RetrieveUpdateAPIView):
    queryset = Feedbacks.objects.all()
    serializer_class = FeedbackReadSerializer


class PatientDetailAPIView(generics.ListAPIView):
    serializer_class = PatientDetailSerializer
    queryset = Patient.objects.all()

    def get_queryset(self):
        return Patient.objects.filter(username=self.request.user)

class DoctorDetailAPIView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer


class DoctorListAPIView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_class = DoctorFilter
    ordering_fields = ['service_price']
    pagination_class = DoctorPagination

class DoctorProfileDetail(generics.RetrieveAPIView):
    serializer_class = DoctorDetailFORDoctorSerializer
    queryset = Doctor.objects.all()
    permission_classes = [CheckDoctorTrue]

class WarningsCreateAPIView(generics.CreateAPIView):
    serializer_class = WarningsSerializer

