from rest_framework import serializers

from core.models import Classroom, Comment, Tutorial


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


class CreateClassroomSerializer(serializers.ModelSerializer):
    """Serialize creating a classroom"""

    class Meta:
        model = Classroom
        fields = ('title', 'description')


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
        fields = ('id', 'owner', 'title', 'description')
        read_only_fields = ('id',)


class ClassroomDetailSerializer(serializers.ModelSerializer):
    """Serialize a classroom detail"""
    videos = TutorialSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)