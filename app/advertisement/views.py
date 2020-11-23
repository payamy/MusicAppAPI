from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Advertisement, User, Tag
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

    def get_serializer_class(self):

        if self.action == 'retrieve':
            return serializers.AdvertisementDetailedSerializer

        return self.serializer_class

class TagViewSet(viewsets.ModelViewSet):
    """Manage tags in database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)