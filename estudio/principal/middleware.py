from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from principal.views import logout_view

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and 'last_activity' in request.session:
            last_activity = request.session['last_activity']
            current_time = timezone.now()
            elapsed_time = current_time - last_activity
            session_timeout = settings.SESSION_COOKIE_AGE

            if elapsed_time.total_seconds() > session_timeout:
                # Tiempo de inactividad excedido, desconecta al usuario y muestra un mensaje
                messages.warning(request, 'Tu sesión ha expirado debido a inactividad.')
                return logout_view(request)

            # Actualiza el temporizador de sesión con el tiempo actual
            request.session['last_activity'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

        return self.get_response(request)