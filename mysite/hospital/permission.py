from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from urllib3 import request


class CheckDoctorTrue(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'doctor':
            return True
        return False

class CheckDoctorFalse(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'doctor':
            return False
        return True


class CheckAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.patiend_id