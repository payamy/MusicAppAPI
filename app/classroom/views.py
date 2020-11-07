from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Comment, User

from classroom import serializers


class AdvertisementViewSet(viewsets.ModelViewSet):
    """Manage comments in classrooms"""
    serializer_class = serializers.CommentSerializer
    queryset = Advertisement.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated)

    def get_queryset(self):
        return self.queryset.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)