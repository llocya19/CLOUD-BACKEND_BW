# app/routes/roles.py

import re
from flask import Blueprint, request, jsonify
from app.database import get_db
from app.models import roles
from app.extensions import cache
roles_bp = Blueprint('roles', __name__)

@roles_bp.route('/api/roles', methods=['GET'])
@cache.cached(timeout=300) 
def listar_roles():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    data = roles.get_all_roles(cursor)
    for rol in data:
        rol['modulos'] = roles.obtener_modulos_por_rol(cursor, rol['id'])
    return jsonify(data)

@roles_bp.route('/api/modulos', methods=['GET'])
@cache.cached(timeout=300) 
def listar_modulos():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    data = roles.get_all_modulos(cursor)
    return jsonify(data)

@roles_bp.route('/api/roles', methods=['POST'])
def agregar_rol():
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    descripcion = data.get('descripcion', '').strip()
    modulos = data.get('modulos', [])

    if not nombre:
        return jsonify({'error': 'El campo "nombre" es obligatorio.'}), 400
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre):
        return jsonify({'error': 'El nombre solo debe contener letras.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    if roles.get_role_by_name(cursor, nombre):
        return jsonify({'error': 'Ya existe un rol con ese nombre.'}), 409

    roles.add_role(cursor, nombre, descripcion)
    rol_id = cursor.lastrowid
    roles.asignar_modulos_a_rol(cursor, rol_id, modulos)
    conn.commit()

    return jsonify({'message': 'Rol creado y modulos asignados exitosamente.'}), 201

@roles_bp.route('/api/roles/<int:id>', methods=['PUT'])
def editar_rol(id):
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    descripcion = data.get('descripcion', '').strip()
    modulos = data.get('modulos', [])

    if not nombre:
        return jsonify({'error': 'El campo "nombre" es obligatorio.'}), 400
    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre):
        return jsonify({'error': 'El nombre solo debe contener letras.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    roles.update_role(cursor, id, nombre, descripcion)
    roles.asignar_modulos_a_rol(cursor, id, modulos)
    conn.commit()

    return jsonify({'message': 'Rol actualizado correctamente.'}), 200

@roles_bp.route('/api/roles/<int:id>', methods=['DELETE'])
def eliminar_rol(id):
    conn = get_db()
    cursor = conn.cursor()
    roles.delete_role(cursor, id)
    conn.commit()
    return jsonify({'message': 'Rol eliminado correctamente.'}), 200
