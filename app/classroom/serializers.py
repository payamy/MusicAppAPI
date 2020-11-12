from rest_framework import serializers

from core.models import Classroom, Comment, Tutorial


class CommentSerializer(serializers.ModelSerializer):
    """Serialize a comment"""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'classroom')
        read_only_fields = ('id',)


class TutorialSerializer(serializers.ModelSerializer):
    """Serialize a video"""

    class Meta:
        model = Tutorial
        fields = ('id', 'title','video', 'description', 'classroom')
        read_only_fields = ('id',)


class ClassroomSerializer(serializers.ModelSerializer):
    """Serialize a classroom"""
    tutorials = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tutorial.objects.all()
    )
    comments = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Comment.objects.all()
    )

    class Meta:
        model = Classroom
        fields = ('id', 'name', 'description', 'tutorials', 'comments')
        read_only_fields = ('id', 'tutorials', 'comments')