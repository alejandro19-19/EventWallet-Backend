from django.db import models

# Create your models here.

TIPO_EVENTO = [
    ('V','Viaje'),
    ('H','Hogar'),
    ('P','Pareja'),
    ('C','Comida'),
    ('O','Otro')

]

class Usuario(models.Model):

    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    apodo = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    foto = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)

class Evento(models.Model):

    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)
    tipo = models.CharField(max_length=1,choices=TIPO_EVENTO)
    foto = models.CharField(max_length=250)
    terminado = models.BooleanField(default=False)

class Actividad(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250)
    valor = models.FloatField()

class Contacto(models.Model):

    usuario1 = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    usuario2 = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        
        unique_together = ('usuario1', 'usuario2')

class Pago (models.Model):

    deudor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    prestador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor = models.FloatField()

class UsuarioParticipaEvento(models.Model):

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    participante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class UsuarioParticipaActividad(models.Model):

    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    participante = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    valor = models.FloatField()
    is_active = models.BooleanField(default=True)

class Invitacion(models.Model):

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    aceptado =  models.BooleanField(default=False)


    

