# backend/routes/usuarios.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.database import get_db
from app.models import usuarios

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    data = usuarios.get_all_users(cursor)
    return jsonify(data)

@usuarios_bp.route('/api/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    email = data.get('email', '').strip()
    estado = data.get('estado', 'activo')
    contraseña = generate_password_hash(data.get('contraseña', '').strip())
    foto = data.get('foto', '')
    roles_ids = data.get('roles', [])

    if not nombre or not email or not data.get('contraseña'):
        return jsonify({'error': 'Todos los campos obligatorios deben completarse.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    if usuarios.get_user_by_email(cursor, email):
        return jsonify({'error': 'Ya existe un usuario con ese correo.'}), 409

    usuarios.add_user(cursor, nombre, email, contraseña, estado, foto)
    usuario_id = cursor.lastrowid
    usuarios.asignar_roles(cursor, usuario_id, roles_ids)
    conn.commit()

    return jsonify({'message': 'Usuario registrado exitosamente.'}), 201

@usuarios_bp.route('/api/usuarios/<int:id>', methods=['PUT'])
def editar_usuario(id):
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    email = data.get('email', '').strip()
    estado = data.get('estado', 'activo')
    foto = data.get('foto', '')
    nueva_contraseña = data.get('nueva_contraseña')
    roles_ids = data.get('roles', [])

    if not nombre or not email:
        return jsonify({'error': 'Nombre y correo son obligatorios.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    if nueva_contraseña:
        hash_contraseña = generate_password_hash(nueva_contraseña)
        usuarios.update_user_with_password(cursor, id, nombre, email, estado, foto, hash_contraseña)
    else:
        usuarios.update_user(cursor, id, nombre, email, estado, foto)

    usuarios.asignar_roles(cursor, id, roles_ids)
    conn.commit()

    return jsonify({'message': 'Usuario actualizado correctamente.'}), 200

@usuarios_bp.route('/api/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    conn = get_db()
    cursor = conn.cursor()
    usuarios.delete_user(cursor, id)
    conn.commit()
    return jsonify({'message': 'Usuario eliminado correctamente.'}), 200

@usuarios_bp.route('/api/roles', methods=['GET'])
def obtener_roles():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    return jsonify(usuarios.get_roles(cursor))

@usuarios_bp.route('/api/usuarios/<int:id>/roles', methods=['GET'])
def obtener_roles_usuario(id):
    conn = get_db()
    cursor = conn.cursor()
    return jsonify(usuarios.get_roles_por_usuario(cursor, id))

@usuarios_bp.route('/api/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    usuario = usuarios.get_user_by_id(cursor, id)

    if usuario:
        usuario['roles'] = usuarios.get_roles_por_usuario(cursor, id)
        usuario['modulos'] = usuarios.get_user_modules(cursor, id)
        return jsonify(usuario), 200
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404
