from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for the creating user object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'user_type')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class EditUserSerializer(serializers.ModelSerializer):
    """Serializer for editing user object"""

    class Meta:
        model = get_user_model()
        fields = ('email' ,'name', 'biography', 'user_type')
        read_only_fields = ('email', 'user_type')
    
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        user = super().update(instance, validated_data)

        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
