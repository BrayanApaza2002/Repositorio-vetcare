import os

from config import config


def get_config():
    """Obtiene la configuración según la variable FLASK_CONFIG."""

    config_name = os.getenv("FLASK_CONFIG", "development")

    selected_config = config.get(config_name)

    if selected_config is None:
        raise ValueError(
            f"Configuración '{config_name}' no válida."
        )

    return selected_config