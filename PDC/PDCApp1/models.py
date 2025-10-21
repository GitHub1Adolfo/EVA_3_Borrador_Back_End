from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    run = models.CharField(max_length=12, unique=True, default="")  # NUEVO CAMPO
    apellido = models.CharField(max_length=50, default="")  # NUEVO CAMPO
    fono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} {self.apellido} - {self.run}"


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50, unique=True, default="0000")
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.raza})"


class Adopcion(models.Model):
    run_cliente = models.CharField(max_length=20)
    nombre_mascota = models.CharField(max_length=100)
    id_mascota = models.CharField(max_length=50)
    detalle = models.TextField(default="Sin detalle")
    fecha_adopcion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre_mascota} adoptada por {self.run_cliente}"
    
# Create your models here.
