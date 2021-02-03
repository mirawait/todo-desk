from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegistartionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64, min_length=1, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=64, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError('Username is required')

        if password is None:
            raise serializers.ValidationError('Password is required')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('There is no required user')

        if not user.is_active:
            raise serializers.ValidationError('This user is disabled')

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
