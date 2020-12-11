from rest_framework import serializers

<<<<<<< HEAD
from core.models import DirectMessage
=======
from core.models import DirectMessage, Chat
>>>>>>> 88b1a9d14182a08f91a17847d3091df0d8d8bd4a


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

