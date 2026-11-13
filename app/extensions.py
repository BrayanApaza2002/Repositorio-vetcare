from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail


# Conexión con la base de datos
db = SQLAlchemy()
mail = Mail()

# Administración de migraciones
migrate = Migrate()

# Administración de sesiones de usuario
login_manager = LoginManager()

# Encriptación de contraseñas
bcrypt = Bcrypt()

# Protección contra ataques CSRF
csrf = CSRFProtect()


# Configuración de Flask-Login
login_manager.login_view = "auth.login"
login_manager.login_message = "Debes iniciar sesión para acceder."
login_manager.login_message_category = "warning"