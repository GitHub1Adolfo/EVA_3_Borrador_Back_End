from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Mascota, Profile, Adopcion

class RegisterForm(UserCreationForm):
    run = forms.CharField(max_length=12, required=True, label="RUN")
    apellido = forms.CharField(max_length=50, required=True, label="Apellido")
    fono = forms.CharField(max_length=20, required=False, label="Teléfono")
    estado = forms.ChoiceField(choices=Profile.ESTADO_CHOICES, required=False, label="Estado")

    class Meta:
        model = User
        fields = ["username", "apellido", "run", "email", "fono", "estado", "password1", "password2"]
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo electrónico',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 5 or len(username) > 20:
            raise forms.ValidationError("El nombre de usuario debe tener entre 5 y 20 caracteres.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email:
            raise forms.ValidationError("El correo debe contener @")
        return email


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'raza', 'identificacion', 'imagen']
        labels = {
            'nombre': 'Nombre de la mascota',
            'raza': 'Raza',
            'identificacion': 'ID o número de registro',
            'imagen': 'Imagen de la mascota',
        }
        
class AdopcionForm(forms.ModelForm):
    class Meta:
        model = Adopcion
        fields = ['run_cliente', 'nombre_mascota', 'id_mascota', 'detalle']
        labels = {
            'run_cliente': 'RUN del Cliente',
            'nombre_mascota': 'Nombre de la Mascota',
            'id_mascota': 'ID de la Mascota',
            'detalle': 'Detalle de la Adopción',
        }
        widgets = {
            'detalle': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe detalles del proceso de adopción...'}),
        }