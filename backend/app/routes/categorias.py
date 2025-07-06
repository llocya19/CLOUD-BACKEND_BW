# routes/categorias.py

from flask import Blueprint, request, jsonify
from app.database import get_db
from app.models import categorias
import re
from app.extensions import cache

categorias_bp = Blueprint('categorias', __name__)

# ✅ Listar todas las categorías
@categorias_bp.route('/api/categorias', methods=['GET'])
def listar_categorias():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    data = categorias.get_all_categorias(cursor)
    return jsonify(data)

# ✅ Agregar una nueva categoría
@categorias_bp.route('/api/categorias', methods=['POST'])
def agregar_categoria():
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    descripcion = data.get('descripcion', '').strip()

    if not nombre:
        return jsonify({'error': 'El nombre es obligatorio.'}), 400

    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre):
        return jsonify({'error': 'El nombre solo debe contener letras y espacios.'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)  # ✅ Corregido
    if categorias.get_categoria_by_nombre(cursor, nombre):
        return jsonify({'error': 'Ya existe una categoría con ese nombre.'}), 409

    categorias.add_categoria(cursor, nombre, descripcion)
    conn.commit()
    return jsonify({'message': 'Categoría registrada exitosamente.'}), 201

# ✅ Editar categoría existente
@categorias_bp.route('/api/categorias/<int:id>', methods=['PUT'])
def editar_categoria(id):
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    descripcion = data.get('descripcion', '').strip()

    if not nombre:
        return jsonify({'error': 'El nombre es obligatorio.'}), 400

    if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', nombre):
        return jsonify({'error': 'El nombre solo debe contener letras y espacios.'}), 400

    conn = get_db()
    cursor = conn.cursor(dictionary=True)  # ✅ Corregido
    existente = categorias.get_categoria_by_nombre(cursor, nombre)

    if existente and existente['id'] != id:
        return jsonify({'error': 'Ya existe una categoría con ese nombre.'}), 409

    categorias.update_categoria(cursor, id, nombre, descripcion)
    conn.commit()
    return jsonify({'message': 'Categoría actualizada correctamente.'}), 200

# ✅ Eliminar categoría por ID
@categorias_bp.route('/api/categorias/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    conn = get_db()
    cursor = conn.cursor()
    categorias.delete_categoria(cursor, id)
    conn.commit()
    return jsonify({'message': 'Categoría eliminada correctamente.'}), 200
