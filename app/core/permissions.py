from rest_framework import permissions

from core.models import User


class TeacherPermission(permissions.BasePermission):
    """Only teachers have permissions to access"""
    
    def has_permission(self, request, view):
        if request.user.user_type == User.Types.TEACHER:
            return True
        return False


class StudentPermission(permissions.BasePermission):
    """Only students have permissions to access"""
    
    def has_permission(self, request, view):
        if request.user.user_type == User.Types.STUDENT:
            return True
        return False