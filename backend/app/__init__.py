from flask import Flask
from flask_cors import CORS
from app.extensions import mail
from app.config import Config
from flask_wtf.csrf import CSRFProtect

# Blueprints
from app.routes.roles import roles_bp
from app.routes.usuarios import usuarios_bp
from app.routes.categorias import categorias_bp
from app.routes.marcas import marcas_bp
from app.routes.productos import productos_bp
from app.routes.clientes import clientes_bp
from app.routes.ventas import ventas_bp
from app.routes.empresa import empresa_bp
from app.routes.boleta import boleta_bp
from app.routes.auth import auth_bp
from app.routes.modulos import modulos_bp
from app.routes.csrf import csrf_bp

csrf = CSRFProtect()  # ✅

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    CORS(app, supports_credentials=True)  # para cookies y CSRF
    mail.init_app(app)
    csrf.init_app(app)  # ✅

    # ✅ Excluir login y OTP del CSRF
    csrf.exempt("login")
    csrf.exempt("verificar_otp")

    # Blueprints
    app.register_blueprint(roles_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(marcas_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(empresa_bp)
    app.register_blueprint(boleta_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(modulos_bp)
    app.register_blueprint(csrf_bp)

    return app
