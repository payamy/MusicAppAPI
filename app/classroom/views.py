from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Classroom, Comment, Tutorial
from core.permissions import TeacherPermission

from classroom import serializers


class BaseClassroomAttrViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage classroom attributes in db"""
    authentication_classes = (TokenAuthentication,)


class CommentViewSet(BaseClassroomAttrViewSet):
    """Manage comments in the database"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticated,)


class TutorialViewSet(BaseClassroomAttrViewSet):
    """Manage tutorials in the database"""
    queryset = Tutorial.objects.all()
    serializer_class = serializers.TutorialSerializer
    permission_classes = (IsAuthenticated, TeacherPermission)


class ClassroomViewSet(viewsets.ModelViewSet):
    """Manage classrooms in database"""
    serializer_class = serializers.ClassroomSerializer
    queryset = Classroom.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, TeacherPermission)

    def get_object(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)