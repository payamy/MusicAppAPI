from rest_framework import serializers

from core.models import Advertisement
from django.conf import settings


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serialize an ad"""
    user_id = serializers.RelatedField(source=settings.AUTH_USER_MODEL, read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'caption', 'user_id')
        read_only_fields = ('id',)