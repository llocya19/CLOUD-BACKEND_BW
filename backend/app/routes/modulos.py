from flask import Blueprint, jsonify
from app.database import get_db
from app.extensions import cache
modulos_bp = Blueprint('modulos', __name__)

@modulos_bp.route('/api/modulos', methods=['GET'])
@cache.cached(timeout=300) 
def listar_modulos():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, ruta FROM modulos ORDER BY id")
    modulos = cursor.fetchall()
    return jsonify(modulos)
