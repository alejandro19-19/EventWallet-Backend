from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

TIPO_EVENTO = [
    ('V','Viaje'),
    ('H','Hogar'),
    ('P','Pareja'),
    ('C','Comida'),
    ('O','Otro')

]

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser, PermissionsMixin):

    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    apodo = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    foto = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'

class Evento(models.Model):

    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='creador_evento')
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)
    tipo = models.CharField(max_length=1,choices=TIPO_EVENTO)
    foto = models.CharField(max_length=250)
    terminado = models.BooleanField(default=False)

class Actividad(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='evento_actividad')
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='creador_actividad')
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)
    valor = models.FloatField()

class Contacto(models.Model):

    usuario1 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario1')
    usuario2 = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario2')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        
        unique_together = ('usuario1', 'usuario2')

class Pago (models.Model):

    deudor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='deudor_pago')
    prestador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='prestador_pago')
    valor = models.FloatField()

class UsuarioParticipaEvento(models.Model):

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='evento_participa')
    participante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='participante_evento')
    is_active = models.BooleanField(default=True)

class UsuarioParticipaActividad(models.Model):

    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE, related_name='actividad_participa')
    participante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='participante_actividad')
    valor = models.FloatField()
    is_active = models.BooleanField(default=True)

class Invitacion(models.Model):

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='invitacion_evento')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_invitacion')
    aceptado =  models.BooleanField(default=False)


    

