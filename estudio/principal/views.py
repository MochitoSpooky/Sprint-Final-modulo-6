from django.shortcuts import render, redirect
from principal.models import Usuario
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UsuarioForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps
from .models import Galeria
from .forms import GaleriaForm


def base(request):
    return render(request, 'principal/base.html')

#subir imagenes a la galeria
def galeria(request):
    images = Galeria.objects.all()
    return render(request, 'principal/galeria.html', {'images': images})

def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            usuario = form.cleaned_data['usuario'] 
            contraseña = form.cleaned_data['contraseña']
            tipo_usuario = form.cleaned_data['tipo_usuario']
            
            # Crea un nuevo usuario
            user = User.objects.create_user(username=usuario, first_name=nombre, last_name=apellido, email=email)
            user.set_password(contraseña)
            user.save()
            
            # Asignar al grupo Moderador o FotoFans según el tipo de usuario elegido
            if tipo_usuario == 'moderador':
                moderador_group = Group.objects.get(name='Moderador')
                moderador_group.user_set.add(user)


            elif tipo_usuario == 'fotofans':
                fotofans_group = Group.objects.get(name='FotoFans')
                fotofans_group.user_set.add(user)
            
            # Redirecciona a la página de inicio
            return redirect('base')
    else:
        form = UsuarioForm()
    
    return render(request, 'principal/crear_usuario.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('perfil')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    
    return render(request, 'principal/login.html')

def logout_view(request):
    logout(request)
    return redirect('base')# Redirecciona a la página principal después del cierre de sesión

from django.shortcuts import render

def profile_view(request):
    user = request.user  # Usuario autenticado
    return render(request, 'principal/perfil.html', {'user': user})

def group_required(*group_names):
    def decorator(view_func):
        @login_required
        def wrapped_view(request, *args, **kwargs):
            if not request.user.groups.filter(name__in=group_names).exists():
                # El usuario no pertenece a ninguno de los grupos especificados, mostrar mensaje de error
                return render(request, 'principal/error_permisos.html')
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

@login_required
@group_required('Moderador')
def lista_usuarios(request):
    usuarios = User.objects.all().prefetch_related('groups')
    return render(request, 'principal/lista_usuarios.html', {'usuarios': usuarios})


@login_required
@group_required('Moderador')
def subir_imagen(request):
    if request.method == 'POST':
        form = GaleriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galeria')
    else:
        form = GaleriaForm()
    return render(request, 'principal/subir_imagen.html', {'form': form})
