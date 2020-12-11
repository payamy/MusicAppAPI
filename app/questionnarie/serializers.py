from rest_framework import serializers

from core.models import Question, Questionnaire, Answer, MultiChoiceAnswer



class Questionnarieserializer(serializers.ModelSerializer):
    """Serialize a questionnarie"""

    class Meta:
        model = Questionnaire
        fields = ('title')

class QuestionSerializer(serializers.ModelSerializer):
    """Serialize a questionnarie"""

    class Meta:
        model = Question
        fields = ('Description', 'type')