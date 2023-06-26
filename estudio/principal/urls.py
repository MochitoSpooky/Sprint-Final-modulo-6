from django.urls import path
from . import views

urlpatterns = [
    path('accounts/profile/', views.profile_view, name='perfil'),

    # Agrega más rutas de URL según sea necesario
]
