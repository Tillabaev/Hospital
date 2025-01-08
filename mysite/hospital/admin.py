from django.contrib import admin
from .models import *

# class SpecialtyInline(admin.TabularInline):
#     model = Specialty
#     extra = 1
#
# class DoctorAdmin(admin.ModelAdmin):
#     inlines = [SpecialtyInline]

class AllergiesInline(admin.TabularInline):
    model = Allergies
    extra = 0

class PatientAdmin(admin.ModelAdmin):
    inlines = [AllergiesInline]

class PrescriptionsInline(admin.TabularInline):
    model  = Prescriptions
    extra = 0

class MedicalRecordAdmin(admin.ModelAdmin):
    inlines = [PrescriptionsInline]


admin.site.register(UserProfile)
admin.site.register(Doctor)
admin.site.register(Specialty)
admin.site.register(Patient,PatientAdmin)
admin.site.register(MedicalRecord,MedicalRecordAdmin)
admin.site.register(Departments)
admin.site.register(Appointments)
admin.site.register(Prescriptions)
admin.site.register(Billings)
admin.site.register(WardsCategory)
admin.site.register(Ward)
admin.site.register(Feedbacks)
admin.site.register(Warnings)