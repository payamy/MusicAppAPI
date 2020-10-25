from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Creating a new user in system"""
    serializer_class = UserSerializer
