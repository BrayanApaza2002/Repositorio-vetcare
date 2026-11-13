
from functools import wraps

from flask import abort
from flask_login import current_user, login_required


def roles_requeridos(*roles):
    """Restringe el acceso a usuarios con determinados roles."""

    def decorador(funcion):

        @wraps(funcion)
        @login_required
        def funcion_protegida(*args, **kwargs):

            if current_user.rol not in roles:
                abort(403)

            return funcion(*args, **kwargs)

        return funcion_protegida

    return decorador
