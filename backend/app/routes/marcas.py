from flask import Blueprint, request, jsonify
from app.database import get_db
from app.models import marcas
import re

marcas_bp = Blueprint('marcas', __name__)

@marcas_bp.route('/api/marcas', methods=['GET'])
def listar_marcas():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    data = marcas.get_all_marcas(cursor)
    return jsonify(data)

@marcas_bp.route('/api/marcas', methods=['POST'])
def agregar_marca():
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    descripcion = data.get('descripcion', '').strip()

    if not nombre:
        return jsonify({'error': 'El nombre es obligatorio.'}), 400

    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre):
        return jsonify({'error': 'El nombre solo debe contener letras y espacios.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    if marcas.get_marca_by_nombre(cursor, nombre):
        return jsonify({'error': 'Ya existe una marca con ese nombre.'}), 409

    marcas.add_marca(cursor, nombre, descripcion)
    conn.commit()
    return jsonify({'message': 'Marca registrada exitosamente.'}), 201

@marcas_bp.route('/api/marcas/<int:id>', methods=['PUT'])
def editar_marca(id):
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    descripcion = data.get('descripcion', '').strip()

    if not nombre:
        return jsonify({'error': 'El nombre es obligatorio.'}), 400

    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre):
        return jsonify({'error': 'El nombre solo debe contener letras y espacios.'}), 400

    conn = get_db()
    cursor = conn.cursor()
    existente = marcas.get_marca_by_nombre(cursor, nombre)
    if existente and existente['id'] != id:
        return jsonify({'error': 'Ya existe una marca con ese nombre.'}), 409

    marcas.update_marca(cursor, id, nombre, descripcion)
    conn.commit()
    return jsonify({'message': 'Marca actualizada correctamente.'}), 200

@marcas_bp.route('/api/marcas/<int:id>', methods=['DELETE'])
def eliminar_marca(id):
    conn = get_db()
    cursor = conn.cursor()
    marcas.delete_marca(cursor, id)
    conn.commit()
    return jsonify({'message': 'Marca eliminada correctamente.'}), 200
