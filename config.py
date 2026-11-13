
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()


# Ruta absoluta del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Ruta fija de la base de datos principal
DATABASE_PATH = BASE_DIR / "instance" / "vetcare.db"


class Config:
    """Configuración general del sistema."""

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "clave-temporal-vetcare"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True

    # Configuración del correo electrónico (Gmail SMTP)
    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp.gmail.com"
    )

    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))

    MAIL_USE_TLS = os.getenv(
        "MAIL_USE_TLS",
        "True"
    ).lower() == "true"

    MAIL_USE_SSL = False

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = os.getenv(
        "MAIL_DEFAULT_SENDER",
        MAIL_USERNAME
    )


class DevelopmentConfig(Config):
    """Configuración para desarrollo."""

    DEBUG = True

    # Utilizar siempre la base de datos principal de VetCare
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + DATABASE_PATH.as_posix()
    )


class ProductionConfig(Config):
    """Configuración para producción."""

    DEBUG = False

    # En producción se exige una clave secreta propia.
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Conexión a PostgreSQL proporcionada por Render.
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    if SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_DATABASE_URI = (
            SQLALCHEMY_DATABASE_URI.replace(
                "postgres://",
                "postgresql://",
                1
            )
        )

class TestingConfig(Config):
    """Configuración para pruebas."""

    TESTING = True

    WTF_CSRF_ENABLED = False

    SQLALCHEMY_DATABASE_URI = "sqlite://"


# Diccionario de configuraciones
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
