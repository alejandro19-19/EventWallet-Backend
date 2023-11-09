from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Usuario, Contacto, Evento, Invitacion, UsuarioParticipaEvento, Actividad, UsuarioParticipaActividad
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

class InvitacionListSerializer(serializers.ModelSerializer):
    evento = EventSerializer(many=False, read_only = True)
    class Meta:
        model = Invitacion
        fields = ("id","evento","usuario","aceptado")

class EventRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsuarioParticipaEvento
        fields = ("evento","participante")

class GetEventSerializer(serializers.ModelSerializer):
    evento = EventSerializer(many=False, read_only = True)
    class Meta:
        model = UsuarioParticipaEvento
        fields = ("evento",)

class ActivitySerializer(serializers.ModelSerializer):
    evento = EventSerializer(many=False, read_only = True)
    class Meta:
        model= Actividad
        fields = ("id", "evento", "nombre", "descripcion", "valor")

class UserInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("id", "nombre", "apellidos", "apodo")

class InvitacionActivitySerializer(serializers.ModelSerializer):
    participante = UserInvitationSerializer(many=False, read_only = True)
    class Meta:
        model = UsuarioParticipaActividad
        fields = ("id", "participante", "actividad", "is_active", "valor")

class GetActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model= Actividad
        fields = ("id", "evento", "nombre", "descripcion", "valor")