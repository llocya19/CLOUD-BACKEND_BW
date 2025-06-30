# backend/app/config.py
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Carpeta para subir imágenes
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'backend', 'uploads')

class Config:
    # Seguridad
    SECRET_KEY = 'clave-super-secreta-llocya-2025'
    WTF_CSRF_ENABLED = True
    WTF_CSRF_METHODS = ["POST", "PUT", "DELETE"]
    
    # Base de datos
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    # API externa
    BACKEND_URL = os.getenv("BACKEND_URL")
    API_TOKEN = os.getenv("API_TOKEN")

    # Archivos permitidos (para imágenes)
    UPLOAD_FOLDER = UPLOAD_FOLDER
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Configuración del correo (Gmail)
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
# Validar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
