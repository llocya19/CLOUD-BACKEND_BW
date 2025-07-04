from flask import Blueprint, request, jsonify
from app.database import get_db
from app.models import empresa as modelo
import os
from werkzeug.utils import secure_filename
from app.extensions import cache
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


empresa_bp = Blueprint('empresa', __name__)

@empresa_bp.route('/api/empresa', methods=['GET'])
@cache.cached(timeout=300) 
def obtener_empresa():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    empresa = modelo.obtener_empresa(cursor)
    return jsonify(empresa)

@empresa_bp.route('/api/empresa', methods=['PUT'])
def actualizar_empresa():
    db = get_db()
    cursor = db.cursor()

    try:
        nombre_comercial = request.form.get('nombre_comercial')
        ruc = request.form.get('ruc')
        direccion = request.form.get('direccion')
        telefono = request.form.get('telefono')
        correo = request.form.get('correo')
        web = request.form.get('web')

        logo = None
        file = request.files.get('logo')
        if file:
            filename = secure_filename(file.filename)
            logo_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(logo_path)
            logo = filename

        data = {
            'nombre_comercial': nombre_comercial,
            'ruc': ruc,
            'direccion': direccion,
            'telefono': telefono,
            'correo': correo,
            'web': web,
            'logo': logo
        }

        modelo.actualizar_empresa(cursor, data)
        db.commit()
        print("🧾 Datos recibidos:", data)

        return jsonify({'mensaje': 'Datos de empresa actualizados'}), 200

    except Exception as e:
        db.rollback()
        print("❌ Error al actualizar empresa:", str(e))  # 👈 agrega esto para ver el error real en consola
        return jsonify({'error': str(e)}), 500

