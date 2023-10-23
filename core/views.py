from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, AuthTokenSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Usuario, Contacto, Evento
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.serializers import UserSerializer, UserModifySerializer, ContactSerializer, GetContactSerializer, EventSerializer
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from django.views.decorators.http import require_http_methods
from django.db.models import Q


#constantes
ERROR_SERIALIZER = "The data sent is not correct"
ERROR_USUARIO_REACTIVADO = "Se ha reactivado el contacto"
ERROR_USUARIO_CONTACTO_EXISTENTE = "El usuario ingresado ya es tu contacto"


class CreateTokenView(ObtainAuthToken):
    """Create auth token"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    # Metodo para crear un usuario
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'error': False,
                'token': token.key,
                'email': user.email,
                'name': user.nombre,
                'apellidos': user.apellidos,
                'created': created,
            },status=status.HTTP_302_FOUND)
        else:
            return Response({"error": True, "informacion": ERROR_SERIALIZER }, status=status.HTTP_400_BAD_REQUEST)

#Clase para crear los usuarios
class CreateUserAdminView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserModifySerializer

    def get_object(self):
        """Retrieve authenticated user"""
        return self.request.user

# Funcion que permite agregar contactos

@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_contact(request):
    user1 = Token.objects.get(key=request.auth.key).user
    try:
        user2 = Usuario.objects.get(email = request.data['email'])
    except Usuario.DoesNotExist:
      return Response({"error": True, "informacion": "El correo ingresado no corresponde a ningun usuario" }, status=status.HTTP_404_NOT_FOUND)
    if user1.id == user2.id:
        return Response({"error": True, "informacion": "No puedes agregarte a ti mismo como contacto" }, status=status.HTTP_400_BAD_REQUEST)
    try:
        if Contacto.objects.get(usuario1_id = user1.id, usuario2_id = user2.id):
     
            aux1 = Contacto.objects.get(usuario1_id = user1.id, usuario2_id = user2.id)
            if aux1.is_active == True:
                return Response({"error": True, "informacion": ERROR_USUARIO_CONTACTO_EXISTENTE }, status=status.HTTP_400_BAD_REQUEST)
            else:
                aux1.is_active = True
                aux1.save()
                return Response({"error": False, "informacion": ERROR_USUARIO_REACTIVADO }, status=status.HTTP_200_OK)  
    except Contacto.DoesNotExist:
        pass

    contacto = Contacto()
    contacto.usuario1_id = user1.id
    contacto.usuario2_id = user2.id
    contacto.save()
    serializer = ContactSerializer(contacto, many=False, context={'request': request})
    return Response(serializer.data,status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@require_http_methods(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def modify_password(request):
    user = Token.objects.get(key=request.auth.key).user
    old_password = request.data['old_password']
    new_password = request.data['new_password']

    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response({"error": False, "informacion": "Se ha modificado la contraseña exitosamente." }, status=status.HTTP_200_OK)
    else:
        return Response({"error": True, "informacion": "La contraseña ingresada no coincide con la anterior." }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@require_http_methods(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deactivate_account(request):
    user = Token.objects.get(key=request.auth.key).user
    password = request.data['password']

    if user.check_password(password):
        if user.is_active == True:
            user.is_active = False
            user.save()
            return Response({"error": False, "informacion": "El usuario se ha deshabilitado" }, status=status.HTTP_200_OK)
        return Response({"error": False, "informacion": "El usuario ya estaba deshabilitado" }, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": True, "informacion": "La contraseña ingresada no es correcta" }, status=status.HTTP_400_BAD_REQUEST)
    
# Funcion que permite listar contactos

@api_view(['GET'])
@require_http_methods(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_contacts(request):
    user = Token.objects.get(key=request.auth.key).user
    user_contacts1 = Contacto.objects.filter(Q(usuario1_id = user.id))
    serializer1 = GetContactSerializer(user_contacts1, many=True, context={'request':request})
    return Response({"error": False, "contacts": serializer1.data} ,status=status.HTTP_200_OK)

@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_contact(request):
    user = Token.objects.get(key=request.auth.key).user
    try:
        user2 = Usuario.objects.get(email = request.data['email'])
    except Usuario.DoesNotExist:
      return Response({"error": True, "informacion": "El correo ingresado no corresponde a ningun usuario" }, status=status.HTTP_404_NOT_FOUND)
    try:
        contacto = Contacto.objects.get(usuario1_id = user.id, usuario2_id = user2.id)
        if contacto.is_active == False:
            return Response({"error": True, "informacion": "Este usuario ya no es tu contacto"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            contacto.is_active=False
            contacto.save()
            return Response({"error": False, "informacion": "El contacto ha sido eliminado" }, status=status.HTTP_200_OK)       
    except Contacto.DoesNotExist:
        return Response({"error": True, "informacion": "Este usuario no es tu contacto"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
def create_event(request):
    user = Token.objects.get(key=request.auth.key).user
    
    evento = Evento()
    evento.creador = user
    evento.nombre = request.data['nombre']
    evento.descripcion = request.data['descripcion']
    evento.tipo = request.data['tipo']
    evento.foto = request.data['foto']
    serializer = EventSerializer(evento, data=request.data, many=False, context={'request': request})
    if serializer.is_valid():
        evento.save()
        return Response({"error": False, "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": True, "informacion": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    