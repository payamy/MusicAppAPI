from rest_framework import serializers

from core.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serialize a comment"""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'like', 'user')
        read_only_fields = ('id',)