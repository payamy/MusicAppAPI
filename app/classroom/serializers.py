from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import Classroom, Comment, Tutorial, User, QuestionAnswer


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


class TeacherSeriliazer(serializers.ModelSerializer):
    """Seriliaze a list of teachers"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'name', 'biography', 'compatibility')
        read_only_fields = ('email', 'name', 'biography')
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        teacher = User.objects.filter(email=instance.email).first()

        user_answer = QuestionAnswer.objects.get_or_create(user=user)[0].answer
        teacher_answer = QuestionAnswer.objects.get_or_create(user=teacher)[0].answer

        print(user_answer)
        print(teacher_answer)

        score = 0
        for i in range(len(user_answer)):
            if user_answer[i] == teacher_answer[i] and user_answer[i] != '0':
                score = score + 1
        print(score)
        instance.compatibility = score
        instance.save()
        return instance
