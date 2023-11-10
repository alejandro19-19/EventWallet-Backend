from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, AuthTokenSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Usuario, Contacto, Evento, Invitacion, UsuarioParticipaEvento, Actividad, UsuarioParticipaActividad
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from core.serializers import UserSerializer, UserModifySerializer, ContactSerializer, GetContactSerializer, EventSerializer, InvitacionSerializer, InvitacionListSerializer, EventRegistrationSerializer, GetEventSerializer, ActivitySerializer, InvitacionActivitySerializer, GetActivitySerializer
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from django.views.decorators.http import require_http_methods


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

# metodo que permite modificar la contraseña

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

# metodo que permite eliminar (desactivar) la cuenta

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
    user_contacts1 = Contacto.objects.filter(usuario1_id = user.id).filter(usuario2__is_active = True)
    serializer = GetContactSerializer(user_contacts1, many=True, context={'request':request})
    return Response({"error": False, "contacts": serializer.data} ,status=status.HTTP_200_OK)

# metodo que permite borrar un contacto (desactivarlo)

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

# metodo que permite crear un evento

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
    try:
        evento.foto = request.data['foto']
    except:
        pass
    serializer = EventSerializer(evento, data=request.data, many=False, context={'request': request})
    if serializer.is_valid():
        evento.save()
        return Response({"error": False, "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": True, "informacion": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# metodo que permite modificar un evento

@api_view(['PUT'])
@require_http_methods(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
def modify_event(request):
    user = Token.objects.get(key=request.auth.key).user

    try:
        evento = Evento.objects.get(id = request.data['evento_id'])
    except Evento.DoesNotExist:
        return Response({"error": True, "informacion": "El id ingresado no corresponde a ningun evento"}, status=status.HTTP_404_NOT_FOUND)
    
    if user.id != evento.creador_id:
         return Response({"error": True, "informacion": "Este solo puede ser modificado por su creador"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        evento.nombre = request.data['nombre']
        evento.descripcion = request.data['descripcion']
        evento.tipo = request.data['tipo']
        try:
            evento.foto = request.data['foto']
        except:
            pass
        serializer = EventSerializer(evento, data=request.data, many=False, context={'request': request})
        if serializer.is_valid():
            evento.save()
            return Response({"error": False, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": True, "informacion": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# metodo que permite crear una invitacion a un evento

@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
def create_invitation(request):
    user = Token.objects.get(key=request.auth.key).user
    try:
        event = Evento.objects.get(id = request.data['evento_id'])
    except Evento.DoesNotExist:
        return Response({"error": True, "informacion": "El id ingresado no corresponde a ningun evento"}, status=status.HTTP_404_NOT_FOUND)
    try:
        user2 = Usuario.objects.get(email = request.data['email'])
        if user.id == user2.id:
            return Response({"error": True, "información":"No puede invitarse asi mismo al evento"}, status=status.HTTP_400_BAD_REQUEST)
    except Usuario.DoesNotExist:
      return Response({"error": True, "informacion": "El correo ingresado no corresponde a ningun usuario" }, status=status.HTTP_404_NOT_FOUND)
    try:
        registro = UsuarioParticipaEvento.objects.get(evento_id = event.id, participante_id = user2.id)
        if registro.is_active == True:
            return Response({"error": True, "información":"El usuario ingresado ya es parte del evento"}, status=status.HTTP_400_BAD_REQUEST)
    except UsuarioParticipaEvento.DoesNotExist:
        pass
    try:
        inv =Invitacion.objects.get(evento_id = event.id, usuario_id = user2.id)
        if inv.is_active == False:
            inv.is_active = True
            inv.save()
            return Response({"error": False, "información":"Se ha reactivado la invitación"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": True, "información":"Este usuario ya ha sido invitado a este evento"}, status=status.HTTP_400_BAD_REQUEST)
    except Invitacion.DoesNotExist:
        pass

    invitacion = Invitacion()
    invitacion.evento_id = event.id
    invitacion.usuario_id = user2.id
    invitacion.save()
    serializer = InvitacionSerializer(invitacion, many=False, context={'request': request})
    return Response({"error": False, "data": serializer.data}, status=status.HTTP_201_CREATED)

# metodo que permite listar las invitaciones a eventos 

@api_view(['GET'])
@require_http_methods(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_invitations(request):
    user = Token.objects.get(key=request.auth.key).user
    user_invitations = Invitacion.objects.filter(usuario_id = user.id, is_active = True)
    serializer = InvitacionListSerializer(user_invitations, many=True, context={'request':request})
    return Response({"error": False, "invitations": serializer.data} ,status=status.HTTP_200_OK)

# metodo que permite aceptar o rechazar una invitacion a un evento

@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def respond_to_invitation(request):
    user = Token.objects.get(key=request.auth.key).user
    try:
        invitacion = Invitacion.objects.get(id= request.data["invitacion_id"])
        if invitacion.is_active == False:
            return Response({"error": True, "informacion": "Esta invitación ya fue respondida" }, status=status.HTTP_400_BAD_REQUEST)
    except Invitacion.DoesNotExist:
        return Response({"error": True, "informacion": "No se encontro ninguna invitación con ese id" }, status=status.HTTP_404_NOT_FOUND)
    
    if request.data["respuesta"]==True:
        invitacion.aceptado = True
        invitacion.is_active = False
        invitacion.save()

        try:
            registro = UsuarioParticipaEvento.objects.get(evento_id = invitacion.evento.id, participante_id = invitacion.usuario.id)
            if registro.is_active == False:
                registro.is_active = True
                registro.save()
                return Response({"error": False, "informacion":"El usuario ha sido agregado al evento"}, status=status.HTTP_200_OK)
        except UsuarioParticipaEvento.DoesNotExist:
            pass

        registro = UsuarioParticipaEvento()
        registro.evento = invitacion.evento
        registro.participante = invitacion.usuario
        registro.save()
        serializer = EventRegistrationSerializer(registro, many=False, context={'request':request})
        return Response({"error": False,"informacion":"Se ha aceptado la invitación y el usuario ha sido añadido al evento","data": serializer.data}, status=status.HTTP_200_OK)
    
    elif request.data["respuesta"]==False:
        invitacion.aceptado = False
        invitacion.is_active = False
        invitacion.save()
        return Response({"error": False,"informacion":"Se ha respondido la invitación"}, status=status.HTTP_200_OK)
    
# metodo que permite listar todos los eventos a los que pertenece el usuario autenticado

@api_view(['GET'])
@require_http_methods(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_events(request):
    user = Token.objects.get(key=request.auth.key).user
    usuario_participa_evento = UsuarioParticipaEvento.objects.filter(participante= user.id)
    serializer1 = GetEventSerializer(
        usuario_participa_evento, many=True, context={'request': request})
    eventos_creador = Evento.objects.filter(creador = user.id)
    serializer2 = EventSerializer(
    eventos_creador, many=True, context={'request': request})
    return Response({"error": False,"eventos_participante":serializer1.data,"eventos_creador":serializer2.data}, status=status.HTTP_200_OK)

# metodo que permite crear actividades

@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
def create_activity(request):
    user = Token.objects.get(key=request.auth.key).user
    try:
        evento = Evento.objects.get(id = request.data['evento'])
    except Evento.DoesNotExist:
      return Response({"error": True, "informacion": "El evento ingresado no existe" }, status=status.HTTP_404_NOT_FOUND)
    
    actividad = Actividad()
    actividad.evento = evento
    actividad.creador = user
    actividad.nombre = request.data['nombre']
    actividad.descripcion = request.data['descripcion']
    actividad.valor = request.data['valor']
    serializer = ActivitySerializer(actividad, data=request.data, many=False, context={'request': request})
    if serializer.is_valid():
        actividad.save()
        return Response({"error": False, "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"error": True, "informacion": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# metodo que permite invitar a un contacto a una actividades

@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
def invitation_activity(request):
    user = Token.objects.get(key=request.auth.key).user
    try:
        actividad = Actividad.objects.get(id = request.data['actividad'])
        participante = Usuario.objects.get(email = request.data['participante'])
        evento = Evento.objects.get(id = actividad.evento.id)
        if user.id != evento.creador.id:
            participante_evento = UsuarioParticipaEvento.objects.filter(evento = evento.id, participante = user.id)
            if not participante_evento.exists():
                return Response({"error": True, "informacion": "No tienes permisos para agregar contactos a esta actividad"}, status=status.HTTP_403_FORBIDDEN)
        if participante.email == actividad.creador.email:
            return Response({"error": True, "informacion": "No puedes agregar al creador de la actividad" }, status=status.HTTP_400_BAD_REQUEST)
        if participante.id != evento.creador.id:
            participa_evento = UsuarioParticipaEvento.objects.filter(evento = evento.id, participante = participante.id)
            if not participa_evento.exists():
                return Response({"error": True, "informacion": "No tienes permisos para agregar contactos a esta actividad"}, status=status.HTTP_403_FORBIDDEN)
    except Actividad.DoesNotExist:
        return Response({"error": True, "informacion": "La actividad ingresada no existe" }, status=status.HTTP_404_NOT_FOUND)
    except Usuario.DoesNotExist:
        return Response({"error": True, "informacion": "El usuario ingresado no existe" }, status=status.HTTP_404_NOT_FOUND)
    try:
        invitacion = UsuarioParticipaActividad.objects.get(participante=participante.id, actividad=request.data['actividad'])
        if invitacion.is_active == False:
            invitacion.is_active = True
            invitacion.save()
            return Response({"error": False, "informacion": "Se ha reactivado la invitacion del usuario en la actividad"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": True, "informacion": "Este usuario ya pertenece a la actividad" }, status=status.HTTP_400_BAD_REQUEST)
    except UsuarioParticipaActividad.DoesNotExist:
        pass

    invitacion = UsuarioParticipaActividad()
    invitacion.actividad = actividad
    invitacion.participante = participante
    serializer = InvitacionActivitySerializer(invitacion, data=request.data, many=False, context={'request': request})
    if serializer.is_valid():
        invitacion.save()
        return Response({"error": False, "data": serializer.data}, status=status.HTTP_200_OK)
    return Response({"error": True, "informacion": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# metodo que permite eliminar una actividades

@api_view(['POST'])
@require_http_methods(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_activity(request):
    user = Token.objects.get(key=request.auth.key).user
    try:
        actividad = Actividad.objects.get(id = request.data['actividad_id'])
    except Actividad.DoesNotExist:
      return Response({"error": True, "informacion": "El id enviado no corresponde a ninguna actividad existente" }, status=status.HTTP_404_NOT_FOUND)
    
    if actividad.creador == user:
        if actividad.is_active == False:
            return Response({"error": True, "informacion": "La actividad fue eliminada con anterioridad"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            actividad.is_active = False
            actividad.save()
            return Response({"error": False, "informacion": "La actividad ha sido eliminada"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": True, "informacion": "Este usuario no tiene permiso para eliminar esta actividad"}, status=status.HTTP_403_FORBIDDEN)

# metodo que permite modificar una actividades

@api_view(['PUT'])
@require_http_methods(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])  
def modify_activity(request):
    user = Token.objects.get(key=request.auth.key).user
    try:
        actividad = Actividad.objects.get(id = request.data['actividad_id'])
    except Actividad.DoesNotExist:
        return Response({"error": True, "informacion": "El id ingresado no corresponde a ninguna actividad"}, status=status.HTTP_404_NOT_FOUND)
    
    if user.id != actividad.creador_id:
         print(user.id)
         print(actividad.creador_id)
         return Response({"error": True, "informacion": "Esta actividad solo puede ser modificada por su creador"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if type(request.data['nombre']) == type(''):
            actividad.nombre = request.data['nombre']
        else:
            return Response({"error": True, "informacion": "tipo de dato (nombre) no valido"}, status=status.HTTP_400_BAD_REQUEST)
        if type(request.data['descripcion']) == type(''):
            actividad.descripcion = request.data['descripcion']
        else:
            return Response({"error": True, "informacion": "tipo de dato (descripcion) no valido"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ActivitySerializer(actividad, many=False, context={'request': request})
        actividad.save()
        return Response({"error": False, "data": serializer.data}, status=status.HTTP_200_OK)
    
# Funcion que permite listar todas las actividades del evento ingresado

@api_view(['GET'])
@require_http_methods(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_activities(request, pk):

    try:
        evento = Evento.objects.get(id = pk)
    except Evento.DoesNotExist:
        return Response({"error": True, "informacion": "El id enviado no corresponde a ningun evento existente" }, status=status.HTTP_404_NOT_FOUND)
        
    activities = Actividad.objects.filter(evento = evento.id, is_active= True)
    serializer = GetActivitySerializer(activities, many=True, context={'request':request})
    return Response({"error": False, "data": serializer.data} ,status=status.HTTP_200_OK)

@api_view(['GET'])
@require_http_methods(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_event_balances(request, pk):

    try:
        evento = Evento.objects.get(id = pk)
    except Evento.DoesNotExist:
        return Response({"error": True, "informacion": "El id enviado no corresponde a ningun evento existente" }, status=status.HTTP_404_NOT_FOUND)
    data = {}

    activities = Actividad.objects.filter(evento = evento.id, is_active= True)

    for actividad in activities:
        id = actividad.id
        participaciones = UsuarioParticipaActividad.objects.filter(actividad_id = id)
        for participacion in participaciones:
            if participacion.is_active:
                participante = Usuario.objects.get(id = participacion.participante_id)
                nombre = participante.nombre + " " + participante.apellidos
                valor = participacion.valor
                if nombre in data:
                    data[nombre] = data[nombre] + [valor]
                else:
                    data[nombre] = [valor]
    
    for i in data:
        valorTotal = 0
        
        for valor in data[i]:
            valorTotal += valor
        data[i] = valorTotal
    dataFinal = {"evento_id":evento.id, "saldos":data}
    
    return Response({"error": False, "data": dataFinal} ,status=status.HTTP_200_OK)