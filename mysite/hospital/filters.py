from django_filters import FilterSet
from .models import *


class DoctorFilter(FilterSet):
    class Meta:
        model = Doctor
        fields = {
            'specialty' : ['exact'],
            'service_price' : ['gt','lt'],
            'working_days' : ['exact'],
            'departments' : ['exact'],
        }
