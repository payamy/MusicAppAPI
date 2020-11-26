from rest_framework import generics, viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Classroom, Comment, Tutorial
from core.permissions import TeacherPermission

from classroom import serializers


class BaseClassroomAttrViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):
    """Manage classroom attributes in db"""
    authentication_classes = (TokenAuthentication,)
        
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CommentViewSet(BaseClassroomAttrViewSet):
    """Manage comments in the database"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TutorialViewSet(BaseClassroomAttrViewSet, generics.RetrieveAPIView):
    """Manage tutorials in the database"""
    queryset = Tutorial.objects.all()
    serializer_class = serializers.TutorialSerializer
    permission_classes = (IsAuthenticated, TeacherPermission)

    def perform_create(self, serializer):

        u = serializer.context['request'].user
        if serializer.validated_data['classroom'] in u.classroom.all():
            serializer.save(user=self.request.user)
        else:
            return Response("Not OK", status=status.HTTP_400_BAD_REQUEST)


class ClassroomViewSet(viewsets.ModelViewSet):
    """Manage classrooms in database"""
    serializer_class = serializers.ClassroomSerializer
    queryset = Classroom.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, TeacherPermission)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ClassroomPublicViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet to all users to use Classrooms"""
    serializer_class = serializers.ClassroomPublicSerializer
    queryset = Classroom.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    