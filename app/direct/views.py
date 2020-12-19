from rest_framework import generics, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from core.models import DirectMessage, Chat


from direct import serializers


class DirectMessageViewSet(viewsets.ModelViewSet):
    """Manage direct messages in database"""
    serializer_class = serializers.DirectMessageSerializer
    queryset = DirectMessage.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

        other_user = serializer.validated_data['reciever']
        if other_user == self.request.user:
            other_user = serializer.validated_data['sender']

        chat_obj = Chat.objects.get_or_create(user=self.request.user)
        chat_obj_other = Chat.objects.get_or_create(user=other_user)

        chat_obj[0].interactors.add(other_user)
        chat_obj_other[0].interactors.add(self.request.user)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of Integers"""
        return[int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Get all messages of a specific user"""
        sender_queryset = self.queryset.filter(sender=self.request.user)
        reciever_queryset = self.queryset.filter(reciever=self.request.user)

        user = self.request.query_params.get('user')

        if user:
            user_id = self._params_to_ints(user)
            sender_queryset = sender_queryset.filter(reciever__id__in=user_id)
            reciever_queryset = reciever_queryset.filter(sender__id__in=user_id)

        return sender_queryset | reciever_queryset


class ChatView(generics.RetrieveAPIView):
    serializer_class = serializers.ChatSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Chat.objects.get(user=self.request.user)
