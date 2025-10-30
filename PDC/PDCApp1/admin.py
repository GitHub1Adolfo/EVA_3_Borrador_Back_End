from django.contrib import admin
from .models import Mascota, Profile, Adopcion, UsuarioRegistrado, Cliente, Solicitud


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'raza', 'identificacion', 'imagen')
    list_filter = ('raza',)
    search_fields = ('nombre', 'raza', 'identificacion')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'run', 'apellido', 'fono', 'estado')
    list_filter = ('estado',)
    search_fields = ('user__username', 'run', 'apellido')


@admin.register(Adopcion)
class AdopcionAdmin(admin.ModelAdmin):
    list_display = ('run_cliente', 'nombre_mascota', 'id_mascota', 'fecha_adopcion')
    list_filter = ('fecha_adopcion',)
    search_fields = ('run_cliente', 'nombre_mascota', 'id_mascota')
    date_hierarchy = 'fecha_adopcion'
    readonly_fields = ('fecha_adopcion',)


@admin.register(UsuarioRegistrado)
class UsuarioRegistradoAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'usuario', 'correo', 'telefono', 'fecha_registro', 'activo')
    list_filter = ('activo', 'fecha_registro')
    search_fields = ('nombres', 'apellidos', 'usuario', 'correo')
    readonly_fields = ('fecha_registro', 'contraseña')
    list_per_page = 25
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombres', 'apellidos', 'correo', 'telefono')
        }),
        ('Cuenta de Usuario', {
            'fields': ('usuario', 'contraseña', 'activo')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Cliente"""
    list_display = ('run_cliente', 'nombre_cliente', 'apellido', 'correo', 'telefono', 'fecha_registro')
    list_filter = ('fecha_registro',)
    search_fields = ('run_cliente', 'nombre_cliente', 'apellido', 'correo')
    readonly_fields = ('fecha_registro',)
    list_per_page = 25
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('run_cliente', 'nombre_cliente', 'apellido')
        }),
        ('Información de Contacto', {
            'fields': ('correo', 'telefono')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_registro',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    """Configuración del administrador para el modelo Solicitud"""
    list_display = ('id', 'run_cliente', 'nombre_mascota', 'estado', 'fecha')
    list_filter = ('estado', 'fecha', 'nombre_mascota')
    search_fields = ('run_cliente__nombre_cliente', 'run_cliente__apellido', 'nombre_mascota__nombre', 'detalle')
    readonly_fields = ('fecha',)
    list_per_page = 25
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información de la Solicitud', {
            'fields': ('run_cliente', 'nombre_mascota', 'estado')
        }),
        ('Detalles', {
            'fields': ('detalle',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha',),
            'classes': ('collapse',)
        }),
    )
    
    # Acciones personalizadas
    actions = ['marcar_como_aprobada', 'marcar_como_rechazada', 'marcar_como_en_proceso']
    
    def marcar_como_aprobada(self, request, queryset):
        """Marca las solicitudes seleccionadas como aprobadas"""
        updated = queryset.update(estado='aprobada')
        self.message_user(request, f'{updated} solicitud(es) marcada(s) como aprobada(s).')
    marcar_como_aprobada.short_description = "Marcar como aprobada"
    
    def marcar_como_rechazada(self, request, queryset):
        """Marca las solicitudes seleccionadas como rechazadas"""
        updated = queryset.update(estado='rechazada')
        self.message_user(request, f'{updated} solicitud(es) marcada(s) como rechazada(s).')
    marcar_como_rechazada.short_description = "Marcar como rechazada"
    
    def marcar_como_en_proceso(self, request, queryset):
        """Marca las solicitudes seleccionadas como en proceso"""
        updated = queryset.update(estado='en_proceso')
        self.message_user(request, f'{updated} solicitud(es) marcada(s) como en proceso.')
    marcar_como_en_proceso.short_description = "Marcar como en proceso"
