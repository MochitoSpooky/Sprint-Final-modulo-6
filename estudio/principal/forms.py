from django import forms
from .models import Galeria
from django.contrib.auth.models import User


class UsuarioForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    email = forms.EmailField()
    usuario = forms.CharField(max_length=100)
    contraseña = forms.CharField(widget=forms.PasswordInput())
    tipo_usuario = forms.ChoiceField(choices=[('moderador', 'Moderador'), ('fotofans', 'FotoFans')])
    
class GaleriaForm(forms.ModelForm):
    class Meta:
        model = Galeria
        fields = ['nombre', 'autor', 'valor', 'imagen']
