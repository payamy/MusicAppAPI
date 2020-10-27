from rest_framework import serializers

from core.models import Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serialize an ad"""

    class Meta:
        model = Advertisement
        fields = ('id', 'caption')
        read_only_fields = ('id',)