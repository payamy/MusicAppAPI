from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Question

from questionnarie import serializers

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.QuestionSerializer
    queryset = Question.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)