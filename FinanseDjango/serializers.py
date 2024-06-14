from rest_framework import serializers


class EditProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    name = serializers.CharField(max_length=100, required=True)
    surname = serializers.CharField(max_length=100, required=True)
