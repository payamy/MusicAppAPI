from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Advertisement, User

from advertisement import serializers


class TeacherPermission(permissions.BasePermission):
    """Only teacher have permissions to post ads"""
    
    def has_permission(self, request, view):
        if request.user.user_type == User.Types.TEACHER:
            return True
        return False


class AdvertisementViewSet(viewsets.ModelViewSet):
    """Manage ads in database"""
    serializer_class = serializers.AdvertisementSerializer
    queryset = Advertisement.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, TeacherPermission)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    