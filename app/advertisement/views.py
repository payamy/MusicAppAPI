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
        

class AdvertisementPublicViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for all users to see Ads"""
    serializer_class = serializers.AdvertisementPublicSerializer
    queryset = Advertisement.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def _params(self, qs):
        """List of string IDs"""
        return [str_id for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve requested Ads for authenticated users"""
        tags = self.request.query_params.get('tags')
        categories = self.request.query_params.get('categories')
        user = self.request.query_params.get('user')
        queryset = self.queryset

        if tags:
            tags_title = self._params(tags)
            queryset = queryset.filter(tags__title__in=tags_title)

        if categories:
            categories_title = self._params(categories)
            queryset = queryset.filter(categories__title__in=categories_title)

        if user:
            user_id = self._params_to_ints(user)
            queryset = queryset.filter(user__id__in=user_id)
        return queryset


class TagViewSet(viewsets.ModelViewSet):
    """Manage tags in database"""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)