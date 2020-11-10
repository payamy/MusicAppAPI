from rest_framework import serializers

from core.models import Classroom, Comment, Tutorial


class CommentSerializer(serializers.ModelSerializer):
    """Serialize a comment"""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'user')
        read_only_fields = ('id',)


class TutorialSerializer(serializers.ModelSerializer):
    """Serialize a video"""

    class Meta:
        model = Tutorial
        fields = ('id', 'video', 'description')
        read_only_fields = ('id',)


class ClassroomSerializer(serializers.ModelSerializer):
    """Serialize a classroom"""
    videos = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tutorial.objects.all()
    )
    comments = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Comment.objects.all()
    )

    class Meta:
        model = Classroom
        fields = ('id', 'title', 'description', 'comments', 'videos')
        read_only_fields = ('id',)


class ClassroomDetailSerializer(ClassroomSerializer):
    """Serialize a classroom detail"""
    videos = TutorialSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)