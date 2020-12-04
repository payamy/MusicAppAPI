from django.http import Http404

from rest_framework import generics, viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Classroom, Comment, Tutorial
from core.permissions import TeacherPermission

from classroom import serializers


class BaseClassroomAttrViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.RetrieveAPIView):
    """Manage classroom attributes in db"""
    authentication_classes = (TokenAuthentication,)


class CommentViewSet(BaseClassroomAttrViewSet):
    """Manage comments in the database"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TutorialViewSet(BaseClassroomAttrViewSet):
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

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


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

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of Integers"""
        return[int(str_id) for str_id in qs.split(',')]
        
    def get_queryset(self):
        """Retrieve requested classes for authenticated users"""
        owner = self.request.query_params.get('owner')
        queryset = self.queryset

        if owner:
            owner_id = self._params_to_ints(owner)
            queryset = queryset.filter(owner__id__in=owner_id)
            
        return queryset
