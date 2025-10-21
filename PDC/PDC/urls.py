"""
URL configuration for PDC project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PDCApp1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('galeria/', views.galeria, name='galeria'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path("register_pet/", views.register_pet, name="register_pet"),
    path("listas/", views.listas, name="listas"),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('eliminar_mascota/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
    path('actualizar_usuario/<int:user_id>/', views.actualizar_usuario, name='actualizar_usuario'),
    path('actualizar_mascota/<int:mascota_id>/', views.actualizar_mascota, name='actualizar_mascota'),
    path('adopcion/', views.crear_adopcion, name='adopcion'),
    path('eliminar_adopcion/<int:adopcion_id>/', views.eliminar_adopcion, name='eliminar_adopcion'),
    path('actualizar_adopcion/<int:adopcion_id>/', views.actualizar_adopcion, name='actualizar_adopcion'),
]