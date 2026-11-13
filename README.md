# 🐾 VetCare – Sistema Web de Gestión Veterinaria

## 📌 Descripción del proyecto

**VetCare** es un sistema web desarrollado para apoyar la administración y gestión de una clínica veterinaria. Su propósito es organizar la información de clientes, mascotas, veterinarios, citas médicas, historiales clínicos, vacunas, pagos y usuarios, facilitando el acceso y control de los datos.

El sistema fue desarrollado como proyecto académico de la carrera de Ingeniería de Sistemas de la Universidad Pública de El Alto (UPEA), utilizando Python y el framework Flask.

## 🎯 Objetivo del proyecto

Desarrollar un sistema web que permita administrar de manera organizada la información y los principales procesos de una clínica veterinaria, mejorando el registro, consulta y seguimiento de los servicios ofrecidos.

## ⚙️ Funcionalidades principales

El sistema cuenta con los siguientes módulos:

- **Autenticación:** inicio y cierre de sesión y control de acceso.
- **Administración:** panel administrativo con indicadores y estadísticas.
- **Usuarios:** registro, consulta, edición y administración de cuentas.
- **Clientes:** registro y administración de los datos de los propietarios.
- **Mascotas:** gestión de información de las mascotas.
- **Veterinarios:** administración de los datos de los profesionales.
- **Citas:** programación y seguimiento de citas veterinarias.
- **Historiales clínicos:** registro y consulta de información médica.
- **Vacunas:** administración de los registros de vacunación.
- **Pagos:** gestión de los pagos correspondientes a los servicios veterinarios.

## 🛠️ Tecnologías utilizadas

| Tecnología | Descripción |
|---|---|
| Python 3.12 | Lenguaje de programación |
| Flask | Framework web |
| SQLite | Base de datos para desarrollo local |
| PostgreSQL | Base de datos para producción |
| SQLAlchemy | ORM para la interacción con la base de datos |
| Flask-SQLAlchemy | Integración de SQLAlchemy con Flask |
| Flask-Migrate | Administración de migraciones |
| Alembic | Control de versiones del esquema de base de datos |
| Flask-Login | Autenticación y sesiones |
| Flask-Bcrypt | Protección de contraseñas |
| Flask-WTF | Formularios y protección CSRF |
| WTForms | Validación y manejo de formularios |
| Bootstrap 5 | Diseño de interfaces |
| HTML, CSS y JavaScript | Desarrollo de las interfaces |
| Chart.js | Visualización de estadísticas |
| Pytest | Pruebas automatizadas |
| Gunicorn | Servidor de aplicaciones para producción |

## 📂 Estructura del proyecto

La aplicación utiliza una arquitectura modular basada en Flask y el patrón Application Factory.

```text
VETCARE/
│
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── config_loader.py
│   │
│   ├── blueprints/
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── citas/
│   │   ├── clientes/
│   │   ├── historiales/
│   │   ├── main/
│   │   ├── mascotas/
│   │   ├── pagos/
│   │   ├── usuarios/
│   │   ├── vacunas/
│   │   └── veterinarios/
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── cita.py
│   │   ├── cliente.py
│   │   ├── historial.py
│   │   ├── mascota.py
│   │   ├── pago.py
│   │   ├── usuario.py
│   │   ├── vacuna.py
│   │   └── veterinario.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       ├── charts.js
│   │       └── main.js
│   │
│   ├── templates/
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── citas/
│   │   ├── clientes/
│   │   ├── historiales/
│   │   ├── main/
│   │   ├── mascotas/
│   │   ├── pagos/
│   │   ├── usuarios/
│   │   ├── vacunas/
│   │   └── veterinarios/
│   │
│   └── utils/
│       ├── decorators.py
│       └── seed.py
│
├── migrations/
│   ├── versions/
│   ├── alembic.ini
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│
├── config.py
├── run.py
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

Los directorios `instance/`, `venv/` y los archivos `.env` se mantienen fuera del repositorio por contener información local o privada.

## 💻 Requisitos previos

Para ejecutar el proyecto se necesita:

- Python 3.12 o una versión compatible.
- pip.
- Git.
- Un navegador web actualizado.

## 🚀 Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

### 2. Ingresar al directorio

```bash
cd VETCARE
```

### 3. Crear un entorno virtual

En Windows PowerShell:

```powershell
python -m venv venv
```

### 4. Activar el entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Instalar las dependencias

```powershell
pip install -r requirements.txt
```

### 6. Configurar las variables de entorno

Crear el archivo `.env` utilizando como referencia `.env.example`:

```powershell
Copy-Item .env.example .env
```

Configurar una clave secreta propia para el entorno local:

```env
FLASK_CONFIG=development
SECRET_KEY=replace-with-a-long-random-secret
```

No publicar el archivo `.env` ni compartir sus valores privados.

### 7. Preparar la base de datos

Ejecutar las migraciones:

```powershell
flask --app run.py db upgrade
```

### 8. Crear la cuenta inicial de administrador

Ejecutar:

```powershell
python -m app.utils.seed
```

El programa solicitará los datos necesarios para registrar la cuenta administrativa.

El primer administrador se crea mediante este procedimiento. Los demás usuarios se administran desde el módulo correspondiente del sistema.

### 9. Iniciar la aplicación

```powershell
python run.py
```

Abrir el navegador y acceder a:

```text
http://127.0.0.1:5000
```

## 🗄️ Base de datos

VetCare utiliza dos alternativas de almacenamiento según el entorno:

- **Desarrollo local:** SQLite.
- **Producción:** PostgreSQL.

La base de datos contempla las siguientes tablas principales:

1. `usuarios`
2. `clientes`
3. `veterinarios`
4. `mascotas`
5. `citas`
6. `historiales`
7. `vacunas`
8. `pagos`

También utiliza `alembic_version` para controlar las versiones de las migraciones.

## 🔐 Seguridad

El sistema incorpora mecanismos básicos de seguridad:

- Autenticación mediante inicio de sesión.
- Gestión de sesiones con Flask-Login.
- Protección de contraseñas mediante hash con Flask-Bcrypt.
- Protección CSRF mediante Flask-WTF.
- Control de acceso basado en roles.
- Configuración mediante variables de entorno.
- Separación de la configuración de desarrollo y producción.

## 🧪 Pruebas automatizadas

El proyecto utiliza Pytest para comprobar el funcionamiento de sus módulos.

Para ejecutar las pruebas:

```powershell
python -m pytest -v
```

## ☁️ Despliegue en Render

El proyecto puede desplegarse como un servicio web en Render.

Configuración general:

| Parámetro | Valor |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn run:app` |
| Configuración Flask | `FLASK_CONFIG=production` |
| Base de datos | PostgreSQL |

Variables de entorno necesarias en producción:

- `FLASK_CONFIG`: `production`
- `SECRET_KEY`: clave secreta segura.
- `DATABASE_URL`: dirección de conexión de PostgreSQL.

Las migraciones deben ejecutarse sobre la base de datos de producción antes de utilizar el sistema.

La base de datos SQLite local no se publica ni se transfiere automáticamente al entorno de producción.

## 👨‍💻 Autor

**Brayan Apaza Alcon**

- Carrera: Ingeniería de Sistemas.
- Universidad: Universidad Pública de El Alto (UPEA).
- Asignatura: Tecnologías Emergentes II.
- Semestre: Séptimo semestre, paralelo C.
- Gestión: 2026.

## 📚 Propósito académico

Este proyecto fue desarrollado con fines académicos como parte de las actividades de la asignatura Tecnologías Emergentes II. Su desarrollo permitió aplicar conocimientos de programación web, diseño de bases de datos, arquitectura modular, autenticación, seguridad y pruebas de software.
