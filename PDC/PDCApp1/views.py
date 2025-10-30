import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, MascotaForm, AdopcionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Mascota, Profile, Adopcion
from django.contrib.auth.models import User
from django.db import IntegrityError

def index(request):
    return render(request, 'mascotas/home.html')

def quienes_somos(request):
    """Vista para la página Quienes Somos - información de la ONG"""
    return render(request, 'mascotas/quienes_somos.html')

def galeria(request):
    images_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
    images = os.listdir(images_dir)
    images = [f'images/{img}' for img in images if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render(request, 'mascotas/galeria.html', {'images': images})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            # Crear el perfil asociado
            Profile.objects.create(
                user=user,
                run=form.cleaned_data['run'],
                apellido=form.cleaned_data['apellido'],
                fono=form.cleaned_data['fono'],
                estado=form.cleaned_data['estado']
            )
            messages.success(request, "✅ Usuario registrado correctamente.")
            # MODIFICADO: Redirige a 'listas' para 'actualización automática'
            return redirect("listas") 
        else:
            messages.error(request, "❌ Error al registrar usuario. Verifica los datos.")
    else:
        form = RegisterForm()
    return render(request, "mascotas/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "mascotas/login.html")

def register_pet(request):
    carpeta_imagenes = os.path.join(settings.BASE_DIR, 'static', 'images')
    imagenes = [f for f in os.listdir(carpeta_imagenes) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Mascota registrada correctamente.") # Añadido
            # MODIFICADO: Redirige a 'listas' para 'actualización automática'
            return redirect('listas') 
    else:
        form = MascotaForm()
    return render(request, 'mascotas/register_pet.html', {'form': form, "imagenes": imagenes})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def listas(request):
    users = User.objects.all()
    profiles = Profile.objects.all()
    user_profiles = []
    profiles_dict = {p.user.id: p for p in profiles}
    for user in users:
        profile = profiles_dict.get(user.id)
        user_profiles.append((user, profile))
    mascotas = Mascota.objects.all()
    adopciones = Adopcion.objects.all().order_by('-fecha_adopcion')
    return render(request, 'mascotas/listas.html', {
        'user_profiles': user_profiles,
        'mascotas': mascotas,
        'adopciones': adopciones
    })

@login_required
def eliminar_usuario(request, user_id):
    if request.user.id == user_id:
        messages.error(request, "No puedes eliminar tu propia cuenta.")
        return redirect('listas')
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, f"Usuario {user.username} eliminado correctamente.")
    return redirect('listas')

@login_required
def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    mascota.delete()
    messages.success(request, f"Mascota {mascota.nombre} eliminada correctamente.")
    return redirect('listas')

@login_required
def actualizar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = Profile.objects.get_or_create(user=user)
    if not request.user.is_staff and request.user != user:
        messages.error(request, "No tienes permiso para editar este usuario.")
        return redirect('listas')
    if request.method == "POST":
        form = RegisterForm(request.POST, instance=user)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.save()
            profile.run = form.cleaned_data.get('run')
            profile.apellido = form.cleaned_data.get('apellido')
            profile.fono = form.cleaned_data.get('fono')
            profile.estado = form.cleaned_data.get('estado')
            profile.save()
            messages.success(request, f"Usuario {user.username} actualizado correctamente.")
            return redirect('listas')
        else:
            messages.error(request, "Error al actualizar el usuario. Verifica los datos.")
    else:
        initial_data = {
            'username': user.username,
            'email': user.email,
            'run': profile.run,
            'apellido': profile.apellido,
            'fono': profile.fono,
            'estado': profile.estado,
        }
        form = RegisterForm(initial=initial_data, instance=user)
    return render(request, "mascotas/update_user.html", {"form": form})

@login_required
def actualizar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    if request.method == "POST":
        form = MascotaForm(request.POST, request.FILES, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, f"Mascota {mascota.nombre} actualizada correctamente.")
            return redirect('listas')
        else:
            messages.error(request, "Error al actualizar la mascota. Verifica los datos.")
    else:
        form = MascotaForm(instance=mascota)
    return render(request, "mascotas/register_pet.html", {"form": form})

@login_required
def crear_adopcion(request):
    if request.method == 'POST':
        form = AdopcionForm(request.POST)
        if form.is_valid():
            adopcion = form.save(commit=False)
            adopcion.save()
            messages.success(request, "✅ Adopción registrada correctamente.")
            return redirect('listas')
        else:
            messages.error(request, "❌ Verifica los datos ingresados. Todos los campos son obligatorios.")
    else:
        form = AdopcionForm()
    return render(request, 'mascotas/adopcion.html', {'form': form})

@login_required
def eliminar_adopcion(request, adopcion_id):
    adopcion = get_object_or_404(Adopcion, id=adopcion_id)
    adopcion.delete()
    messages.success(request, f"Adopción de {adopcion.nombre_mascota} eliminada correctamente.")
    return redirect('listas')

@login_required
def actualizar_adopcion(request, adopcion_id):
    adopcion = get_object_or_404(Adopcion, id=adopcion_id)
    if request.method == 'POST':
        run_cliente = request.POST.get('run_cliente')
        nombre_mascota = request.POST.get('nombre_mascota')
        id_mascota = request.POST.get('id_mascota')
        detalle = request.POST.get('detalle')
        if not run_cliente or not nombre_mascota or not id_mascota:
            messages.error(request, "⚠️ Todos los campos son obligatorios.")
            return redirect('actualizar_adopcion', adopcion_id=adopcion.id)
        adopcion.run_cliente = run_cliente
        adopcion.nombre_mascota = nombre_mascota
        adopcion.id_mascota = id_mascota
        adopcion.detalle = detalle
        adopcion.save()
        messages.success(request, f"✅ Adopción de {adopcion.nombre_mascota} actualizada correctamente.")
        return redirect('listas')
    context = {
        'adopcion': adopcion
    }
    return render(request, 'mascotas/actualizar_adopcion.html', context)