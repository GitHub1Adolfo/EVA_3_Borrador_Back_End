from django.contrib import admin
from .models import Mascota, Profile

@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'raza', 'identificacion', 'imagen')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fono', 'estado')
