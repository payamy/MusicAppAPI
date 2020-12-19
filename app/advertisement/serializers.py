from rest_framework import serializers

from core.models import Advertisement, Tag
from django.conf import settings


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serialize an ad"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'caption', 'image', 'tags', 'categories')
        read_only_fields = ('id',)


class AdvertisementPublicSerializer(serializers.ModelSerializer):
    """Serialize ads for all users"""

    class Meta:
        model = Advertisement
        fields = ('id', 'user','caption', 'image', 'tags', 'categories')


class TagSerializer(serializers.ModelSerializer):
    """Serialize a tag"""

    class Meta:
        model = Tag
        fields = ('title',)


class AdvertisementDetailedSerializer(AdvertisementSerializer):
    tags = TagSerializer(many=True, read_only=True)