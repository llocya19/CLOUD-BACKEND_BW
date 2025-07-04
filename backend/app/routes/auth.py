from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash
from app.database import get_db
from app.utils.otp import crear_y_enviar_otp
from app.models import usuarios

# ✅ Ruta base /api para todas las rutas del auth
auth_bp = Blueprint('auth', __name__, url_prefix='/api')


@auth_bp.route('/login', methods=['POST'], endpoint='login')
def login():
    data = request.get_json()
    email = data.get('email')
    contraseña = data.get('contraseña')

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user or not check_password_hash(user['contraseña'], contraseña):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    if user['estado'] != 'activo':
        return jsonify({'error': 'Cuenta inactiva'}), 403

    crear_y_enviar_otp(user['id'], user['email'], user['nombre'])

    return jsonify({'message': 'OTP enviado', 'user_id': user['id']}), 200


@auth_bp.route('/verificar-otp', methods=['POST'], endpoint='verificar_otp')
def verificar_otp():
    data = request.get_json()
    user_id = data.get('user_id')
    otp_ingresado = data.get('otp')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM otps 
        WHERE usuario_id = %s AND otp = %s AND expires_at > NOW() AND verificado = 0
    """, (user_id, otp_ingresado))
    otp_data = cursor.fetchone()
    
    if not otp_data:
        return jsonify({'error': 'Código inválido o expirado'}), 401
    
    cursor.execute("UPDATE otps SET verificado = 1 WHERE id = %s", (otp_data['id'],))
    db.commit()

    # Obtener datos del usuario + rol
    cursor.execute("""
        SELECT 
            u.id, u.nombre, u.email, u.foto, u.estado,
            GROUP_CONCAT(r.nombre SEPARATOR ', ') AS rol
        FROM usuarios u
        LEFT JOIN usuarios_roles ur ON u.id = ur.usuario_id
        LEFT JOIN roles r ON ur.rol_id = r.id
        WHERE u.id = %s
        GROUP BY u.id
    """, (user_id,))
    user = cursor.fetchone()

    user['modulos'] = usuarios.get_user_modules(cursor, user_id)

    return jsonify({'message': 'OTP verificado', 'user': user}), 200


@auth_bp.route('/logout', methods=['POST'], endpoint='logout')
def logout():
    session.clear()
    return jsonify({'message': 'Sesión cerrada exitosamente'}), 200
