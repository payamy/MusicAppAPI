
from rest_framework import serializers

from core.models import Question, QuestionChoice, QuestionAnswer


class QuestionSerializer(serializers.ModelSerializer):
    """Serialize a questionnarie"""

    questionchoice = serializers.PrimaryKeyRelatedField(
    	many=True,
    	read_only=True)

    class Meta:
        model = Question
        fields = ('id','title', 'answer', 'questionchoice')


class QuestionAnswerSerializer(serializers.ModelSerializer):
    """Serialize answer to Questionnarie"""

    class Meta:
        model = QuestionAnswer
        fields = ('answer',)