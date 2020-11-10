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
    permission_classes = (IsAuthenticated)

    def get_queryset(self):
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


class CreateClassroomViewSet(generics.CreateAPIView):
    """Create classrooms in database"""
    serializer_class = serializers.CreateClassroomSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, TeacherPermission)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ManageClassroomViewSet(generics.RetrieveUpdateAPIView):
    """Manage classrooms in database"""
    serializer_class = serializers.ClassroomSerializer
    queryset = Classroom.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, TeacherPermission)

    def get_object(self):
        return self.queryset.filter(user=self.request.user)


class ClassroomViewSet(generics.RetrieveAPIView):
    """Visit classrooms"""
    serializer_class = serializers.ClassroomDetailSerializer
    queryset = Classroom.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
