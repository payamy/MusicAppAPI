from rest_framework import viewsets, generics, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Question, QuestionAnswer

from questionnarie import serializers

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
   serializer_class = serializers.QuestionSerializer
   queryset = Question.objects.all()
   authentication_classes = (TokenAuthentication,)
   permission_classes = (IsAuthenticated,)


class QuestionAnswerView(generics.RetrieveUpdateAPIView):
   serializer_class = serializers.QuestionAnswerSerializer
   authentication_classes = (TokenAuthentication,)
   permission_classes = (IsAuthenticated,)

   def get_object(self):
      answer = QuestionAnswer.objects.get_or_create(user=self.request.user)
      return answer[0]
