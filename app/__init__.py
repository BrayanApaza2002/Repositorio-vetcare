
from flask import Flask

from app.config_loader import get_config
from app.extensions import (
    db,
    migrate,
    login_manager,
    bcrypt,
    csrf,
    mail
)

from app.blueprints.main import bp as main_bp
from app.blueprints.auth import bp as auth_bp
from app.blueprints.admin import bp as admin_bp
from app.blueprints.clientes import bp as clientes_bp
from app.blueprints.mascotas import bp as mascotas_bp
from app.blueprints.veterinarios import bp as veterinarios_bp
from app.blueprints.citas import bp as citas_bp
from app.blueprints.historiales import bp as historiales_bp
from app.blueprints.vacunas import bp as vacunas_bp
from app.blueprints.pagos import bp as pagos_bp
from app.blueprints.usuarios import bp as usuarios_bp

from app.models import Usuario


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(Usuario, int(user_id))
    except (ValueError, TypeError):
        return None


def create_app():

    app = Flask(__name__)

    app.config.from_object(get_config())

    # Validar variables obligatorias en producción.
    if app.config.get("DEBUG") is False:

        if not app.config.get("SECRET_KEY"):
            raise RuntimeError(
                "Falta configurar SECRET_KEY en producción."
            )

        if not app.config.get("SQLALCHEMY_DATABASE_URI"):
            raise RuntimeError(
                "Falta configurar DATABASE_URL en producción."
            )

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)

    # Registrar Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(mascotas_bp)
    app.register_blueprint(veterinarios_bp)
    app.register_blueprint(citas_bp)
    app.register_blueprint(historiales_bp)
    app.register_blueprint(vacunas_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(usuarios_bp)

    return app
