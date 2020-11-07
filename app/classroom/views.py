from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Comment, Tutorial

from classroom import serializers


class BaseClassroomAttrViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage classroom attributes in db"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated)

    def get_queryset(self):
        """Return objects for current authenticated users only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(BaseClassroomAttrViewSet):
    """Manage comments in the database"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer


class TutorialViewSet(BaseClassroomAttrViewSet):
    """Manage tutorials in the database"""
    queryset = Tutorial.objects.all()
    serializer_class = serializers.TutorialSerializer