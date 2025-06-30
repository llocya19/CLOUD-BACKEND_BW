# backend/app/routes/productos.py
from flask import Blueprint, request, jsonify, current_app
from app.models import productos
from app.database import get_db
from werkzeug.utils import secure_filename
from app.config import allowed_file
import os

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/api/productos', methods=['GET'])
def listar_productos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    lista = productos.obtener_todos(cursor)
    return jsonify(lista), 200

@productos_bp.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    producto = productos.obtener_por_id(cursor, id)
    return jsonify(producto), 200 if producto else 404

@productos_bp.route('/api/productos', methods=['POST'])
def crear_productos():
    db = get_db()
    cursor = db.cursor()
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({'error': 'Se esperaba una lista de productos'}), 400

    try:
        for item in data:
            # Validaciones backend
            if not item.get('nombre') or not item['nombre'].strip():
                return jsonify({'error': 'El nombre es obligatorio'}), 400
            if not item.get('codigo_barra') or not item['codigo_barra'].strip():
                return jsonify({'error': 'El código de barra es obligatorio'}), 400
            if float(item.get('precio_unitario', 0)) <= 0:
                return jsonify({'error': 'El precio debe ser mayor a cero'}), 400
            if int(item.get('stock_inicial', 0)) <= 0:
                return jsonify({'error': 'El stock inicial debe ser mayor a cero'}), 400
            if int(item.get('cantidad_disponible', 0)) <= 0:
                return jsonify({'error': 'La cantidad disponible debe ser mayor a cero'}), 400

            # Verificar duplicados
            cursor.execute("SELECT COUNT(*) FROM productos WHERE nombre = %s", (item['nombre'],))
            if cursor.fetchone()[0] > 0:
                return jsonify({'error': f"El nombre '{item['nombre']}' ya está registrado"}), 400

            cursor.execute("SELECT COUNT(*) FROM productos WHERE codigo_barra = %s", (item['codigo_barra'],))
            if cursor.fetchone()[0] > 0:
                return jsonify({'error': f"El código de barra '{item['codigo_barra']}' ya está registrado"}), 400

            productos.crear_producto(cursor, item)

        db.commit()
        return jsonify({'mensaje': 'Productos registrados correctamente'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/api/productos/<int:id>', methods=['PUT'])
def editar_producto(id):
    db = get_db()
    cursor = db.cursor()

    data = request.form.to_dict()
    imagen = request.files.get('imagen')

    if imagen and imagen.filename != '':
        if not allowed_file(imagen.filename):
            return jsonify({'error': 'Formato de imagen no permitido'}), 400

        filename = secure_filename(imagen.filename)
        ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        imagen.save(ruta_guardado)
        data['imagen'] = f'/uploads/{filename}'
    else:
        cursor.execute("SELECT imagen FROM productos WHERE id = %s", (id,))
        resultado = cursor.fetchone()
        data['imagen'] = resultado[0] if resultado else ''

    try:
        productos.actualizar_producto(cursor, id, data)
        db.commit()
        return jsonify({'mensaje': 'Producto actualizado correctamente'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    db = get_db()
    cursor = db.cursor()
    try:
        productos.eliminar_producto(cursor, id)
        db.commit()
        return jsonify({'mensaje': 'Producto eliminado correctamente'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/api/productos/upload', methods=['POST'])
def crear_producto_con_imagen():
    db = get_db()
    cursor = db.cursor()

    imagen = request.files.get('imagen')
    data = request.form.to_dict()

    if imagen and imagen.filename != '':
        if not allowed_file(imagen.filename):
            return jsonify({'error': 'Formato de imagen no permitido'}), 400

        filename = secure_filename(imagen.filename)
        ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        imagen.save(ruta_guardado)
        data['imagen'] = f"/uploads/{filename}"
    else:
        data['imagen'] = ''

    try:
        productos.crear_producto(cursor, data)
        db.commit()
        return jsonify({'mensaje': 'Producto registrado'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@productos_bp.route('/api/productos/duplicado', methods=['GET'])
def verificar_duplicado_producto():
    campo = request.args.get('campo')
    valor = request.args.get('valor')

    if campo not in ['nombre', 'codigo_barra']:
        return jsonify({'error': 'Campo inválido'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM productos WHERE {campo} = %s", (valor,))
    existe = cursor.fetchone()[0] > 0

    return jsonify({'existe': existe}), 200
@productos_bp.route('/api/productos/por-codigo/<codigo_barra>', methods=['GET'])
def buscar_producto_por_codigo_barra(codigo_barra):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE codigo_barra = %s", (codigo_barra,))
    producto = cursor.fetchone()

    if producto:
        return jsonify(producto), 200
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404

@productos_bp.route('/api/productos/stock-bajo', methods=['GET'])
def productos_stock_bajo():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, nombre, cantidad_disponible
        FROM productos
        WHERE cantidad_disponible <= 5
    """)
    productos_bajo_stock = cursor.fetchall()
    return jsonify(productos_bajo_stock), 200
