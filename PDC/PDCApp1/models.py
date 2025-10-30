from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone

class Profile(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    run = models.CharField(max_length=12, unique=True, default="")
    apellido = models.CharField(max_length=50, default="")
    fono = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} {self.apellido} - {self.run}"


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50, unique=True, default="0000")
    imagen = models.ImageField(upload_to='images/', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)  # AÑADIDO

    def __str__(self):
        return f"{self.nombre} ({self.raza})"
    
    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"


class Adopcion(models.Model):
    run_cliente = models.CharField(max_length=20)
    nombre_mascota = models.CharField(max_length=100)
    id_mascota = models.CharField(max_length=50)
    detalle = models.TextField(default="Sin detalle")
    fecha_adopcion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre_mascota} adoptada por {self.run_cliente}"
    
    class Meta:
        verbose_name = "Adopción"
        verbose_name_plural = "Adopciones"
        ordering = ['-fecha_adopcion']


# NUEVO: Modelo para usuarios registrados (alternativo al sistema User)
class UsuarioRegistrado(models.Model):
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    correo = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    usuario = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Usuario")
    contraseña = models.CharField(max_length=128, verbose_name="Contraseña")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    activo = models.BooleanField(default=True, verbose_name="Usuario Activo")
    
    def save(self, *args, **kwargs):
        # Encriptar la contraseña antes de guardar
        if self.contraseña and not self.contraseña.startswith('pbkdf2_'):
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.usuario})"
    
    class Meta:
        verbose_name = "Usuario Registrado"
        verbose_name_plural = "Usuarios Registrados"
        ordering = ['-fecha_registro']


# NUEVO: Modelo Cliente (para sistema de administración)
class Cliente(models.Model):
    run_cliente = models.CharField(max_length=10, unique=True, verbose_name="RUN Cliente")
    nombre_cliente = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    correo = models.TextField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=12, verbose_name="Teléfono")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    
    def __str__(self):
        return f"{self.nombre_cliente} {self.apellido} - {self.run_cliente}"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-fecha_registro']


# NUEVO: Modelo Solicitud
class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    
    run_cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.CASCADE, 
        verbose_name="Cliente",
        related_name="solicitudes"
    )
    nombre_mascota = models.ForeignKey(
        Mascota, 
        on_delete=models.CASCADE, 
        verbose_name="Mascota",
        related_name="solicitudes"
    )
    detalle = models.TextField(verbose_name="Detalle de la Solicitud")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Solicitud")
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='pendiente',
        verbose_name="Estado"
    )
    
    def __str__(self):
        return f"Solicitud #{self.id} - {self.run_cliente.nombre_cliente} - {self.nombre_mascota.nombre}"
    
    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        ordering = ['-fecha']