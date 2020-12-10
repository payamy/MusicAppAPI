from rest_framework import serializers

from core.models import DirectMessage, Chat


class DirectMessageSerializer(serializers.ModelSerializer):
    """Serializing messages between users"""
    class Meta:
        model = DirectMessage
        fields = ('sender', 'reciever', 'text', 'datetime')
        read_only_fields = ('sender',)

    
class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('interactors',)