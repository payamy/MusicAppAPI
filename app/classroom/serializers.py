from rest_framework import serializers

from core.models import Comment, Tutorial


class CommentSerializer(serializers.ModelSerializer):
    """Serialize a comment"""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'like', 'user')
        read_only_fields = ('id',)


class TutorialSerializer(serializers.ModelSerializer):
    """Serialize a video"""

    class Meta:
        model = Tutorial
        fields = ('id', 'video', 'description')
        read_only_fields = ('id',)