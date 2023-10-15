from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Usuario
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
        fields = ("id","nombre", "apellidos","apodo","password", "email", "foto" )
    
    def create(self, validated_data):
        user = Usuario(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

class UserModifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ("id", "nombre", "apellidos", "apodo", "password", "foto" )

    def update(self, instance, validated_data):
        # Verificar si la contraseña está presente en los datos validados
        if 'password' in validated_data:
            nueva_contraseña = validated_data['password']
            #obtiene el usuario actual
            user = Usuario.objects.get(pk=instance.pk)
            user.set_password(nueva_contraseña)
            user.save()
            return user