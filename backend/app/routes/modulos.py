from flask import Blueprint, jsonify
from app.database import get_db

modulos_bp = Blueprint('modulos', __name__)

@modulos_bp.route('/api/modulos', methods=['GET'])
def listar_modulos():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, ruta FROM modulos ORDER BY id")
    modulos = cursor.fetchall()
    return jsonify(modulos)
