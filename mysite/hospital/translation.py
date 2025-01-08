from .models import *
from modeltranslation.translator import TranslationOptions,register

@register(MedicalRecord)
class MedicalRecordTranslationOptions(TranslationOptions):
    fields = ('diagnosis', 'treatment')

@register(Allergies)
class AllergiesTranslationOptions(TranslationOptions):
    fields = ('allergies',)


# @register(MedicalRecord)
# class PrescriptionsTranslationOptions(TranslationOptions):
#     fields = ('diagnosis', 'treatment')
