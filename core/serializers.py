from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Usuario, Contacto, Evento, Invitacion
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
        fields = ("id", "nombre", "apellidos", "apodo", "password", "email", "foto" )
    
    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("id", "nombre", "apellidos", "apodo", "foto" )

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = ("id", "usuario1", "usuario2", "is_active")

class UserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "nombre", "apellidos", "apodo", "email", "foto" )

class GetContactSerializer(serializers.ModelSerializer):
    usuario2 = UserContactSerializer(many=False, read_only = True)

    class Meta:
        model = Contacto
        fields = ("id", "usuario1", "usuario2", "is_active")

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ("id","nombre", "descripcion", "tipo", "foto")

class InvitacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitacion
        fields = ("id","evento","usuario","aceptado")