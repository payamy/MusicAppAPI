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
        read_only=True
    )
    comments = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Classroom
        fields = ('id', 'name', 'description', 'tutorials', 'comments')
        read_only_fields = ('id',)


class ClassroomPublicSerializer(serializers.ModelSerializer):
    """Serializer Classroom for all users"""
    tutorials = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='classroom:tutorial-detail'
    )
    comments = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='classroom:comment-detail'
    )

    class Meta:
        model = Classroom
        fields = ('id', 'owner', 'name', 'description' , 'tutorials', 'comments')