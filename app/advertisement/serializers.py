from rest_framework import serializers

from core.models import Advertisement, Tag
from django.conf import settings


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serialize an ad"""

    class Meta:
        model = Advertisement
        fields = ('id', 'caption', 'image')
        read_only_fields = ('id',)


class TagSerializer(serializers.ModelSerializer):
    """Serialize a tag"""

    class Meta:
        model = Tag
        fields = ('title',)