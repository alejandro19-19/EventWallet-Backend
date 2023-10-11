from rest_framework import serializers
from django.contrib.auth import get_user_model
#from core.models import

class AuthTokenSerializer(serializers.Serializer):
    """serializer for the user authentication objectt"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("nombre", "apellidos","apodo","password", "email", "foto" )
