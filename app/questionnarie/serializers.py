
from rest_framework import serializers

from core.models import Question, QuestionChoice




class QuestionSerializer(serializers.ModelSerializer):
    """Serialize a questionnarie"""

    questionchoice = serializers.PrimaryKeyRelatedField(
    	many=True,
    	read_only=True)

    class Meta:
        model = Question
        fields = ('id','title', 'answer', 'questionchoice')
        read_only_fields = ('id','title', 'questionchoice')