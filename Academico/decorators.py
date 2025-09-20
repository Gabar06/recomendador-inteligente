from functools import wraps
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from .models import Usuario

def role_login_required(expected_role, login_url_name):
    """
    expected_role: Usuario.DOCENTE o Usuario.ESTUDIANTE
    login_url_name: 'login_docente' o 'login_estudiante'
    """
    def deco(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            login_url = reverse(login_url_name)
            next_qs = f"?next={request.get_full_path()}"
            # 1) No autenticado -> al login específico
            if not request.user.is_authenticated:
                return redirect(login_url + next_qs)

            u = request.user
            # 2) Chequeo de rol (soporta campo role o perfiles OneToOne)
            ok = False
            if hasattr(u, "role") and u.role:
                ok = (u.role == expected_role)
            else:
                ok = (expected_role == Usuario.DOCENTE and hasattr(u, "docente")) or \
                     (expected_role == Usuario.ESTUDIANTE and hasattr(u, "estudiante"))

            # 3) Rol incorrecto -> logout y login del rol correcto
            if not ok:
                logout(request)
                return redirect(login_url + next_qs)

            return view_func(request, *args, **kwargs)
        return _wrapped
    return deco