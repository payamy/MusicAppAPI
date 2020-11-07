from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Advertisement, User
from core.permissions import TeacherPermission

from advertisement import serializers


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
    