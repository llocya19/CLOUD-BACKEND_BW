# backend/app/models/clientes.py
from app.utils.api_clientes import consultar_dni_api





# backend/app/routes/clientes.py

from flask import Blueprint, request, jsonify
from app.models import clientes
from app.database import get_db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/api/clientes', methods=['GET'])
def listar_clientes():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    resultado = clientes.obtener_todos(cursor)
    return jsonify(resultado), 200

@clientes_bp.route('/api/clientes/<int:id>', methods=['GET'])
def obtener_cliente(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    resultado = clientes.obtener_por_id(cursor, id)
    return jsonify(resultado), 200 if resultado else 404

@clientes_bp.route('/api/clientes/duplicado', methods=['GET'])
def verificar_duplicado():
    campo = request.args.get('campo')
    valor = request.args.get('valor')

    if campo not in ['email', 'dni','ruc']:
        return jsonify({'error': 'Campo no permitido'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM clientes WHERE {campo} = %s", (valor,))
    existe = cursor.fetchone()[0] > 0
    return jsonify({'existe': existe}), 200

@clientes_bp.route('/api/clientes/guardar', methods=['POST'])
def guardar_lote_clientes():
    db = get_db()
    cursor = db.cursor()
    datos = request.get_json()

    if not isinstance(datos, list):
        return jsonify({'error': 'Se esperaba una lista de clientes'}), 400

    try:
        for data in datos:
            # Validaciones generales
            obligatorios = ['nombre', 'email', 'telefono', 'direccion', 'tipo_cliente']
            for campo in obligatorios:
                if not data.get(campo):
                    return jsonify({'error': f'El campo {campo} es obligatorio'}), 400

            # Validar tipo_cliente específico
            tipo = data['tipo_cliente']
            if tipo == 'persona':
                if not data.get('dni') or len(data['dni']) != 8:
                    return jsonify({'error': 'El DNI es obligatorio y debe tener 8 dígitos'}), 400
            elif tipo == 'empresa':
                if not data.get('ruc') or len(data['ruc']) < 8:
                    return jsonify({'error': 'El RUC es obligatorio para empresas'}), 400
            else:
                return jsonify({'error': 'Tipo de cliente inválido'}), 400

            # Verificar duplicados
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE email = %s", (data['email'],))
            if cursor.fetchone()[0] > 0:
                return jsonify({'error': f"El email '{data['email']}' ya está registrado."}), 400

            if tipo == 'persona':
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE dni = %s", (data['dni'],))
                if cursor.fetchone()[0] > 0:
                    return jsonify({'error': f"El DNI '{data['dni']}' ya está registrado."}), 400
            if tipo == 'empresa':
                cursor.execute("SELECT COUNT(*) FROM clientes WHERE ruc = %s", (data['ruc'],))
                if cursor.fetchone()[0] > 0:
                    return jsonify({'error': f"El RUC '{data['ruc']}' ya está registrado."}), 400


            clientes.crear_cliente(cursor, data)

        db.commit()
        return jsonify({'mensaje': 'Clientes registrados correctamente'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@clientes_bp.route('/api/clientes/<int:id>', methods=['PUT'])
def editar_cliente(id):
    db = get_db()
    cursor = db.cursor()
    data = request.get_json()

    try:
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE email = %s AND id != %s", (data['email'], id))
        if cursor.fetchone()[0] > 0:
            return jsonify({'error': f"El email '{data['email']}' ya está en uso."}), 400

        cursor.execute("SELECT COUNT(*) FROM clientes WHERE dni = %s AND id != %s", (data['dni'], id))
        if cursor.fetchone()[0] > 0:
            return jsonify({'error': f"El DNI '{data['dni']}' ya está en uso."}), 400
        cursor.execute("SELECT COUNT(*) FROM clientes WHERE ruc = %s AND id != %s", (data['ruc'], id))
        if cursor.fetchone()[0] > 0:
            return jsonify({'error': f"El RUC '{data['ruc']}' ya está en uso."}), 400


        clientes.actualizar_cliente(cursor, id, data)
        db.commit()
        return jsonify({'mensaje': 'Cliente actualizado correctamente'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500

@clientes_bp.route('/api/clientes/<int:id>', methods=['DELETE'])
def eliminar_cliente(id):
    db = get_db()
    cursor = db.cursor()
    try:
        clientes.eliminar_cliente(cursor, id)
        db.commit()
        return jsonify({'mensaje': 'Cliente eliminado correctamente'}), 200
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
@clientes_bp.route('/api/clientes/por-documento/<numero>', methods=['GET'])
def obtener_cliente_por_documento(numero):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Buscar en la base de datos
    if len(numero) == 8:
        cursor.execute("SELECT id, nombre, dni, direccion FROM clientes WHERE dni = %s", (numero,))
    else:
        cursor.execute("SELECT id, nombre, ruc, direccion FROM clientes WHERE ruc = %s", (numero,))
    
    cliente = cursor.fetchone()
    if cliente:
        return jsonify(cliente), 200
    
    # Si no se encuentra, consultar API externa
    externo = consultar_dni_api(numero)
    if externo:
        return jsonify(externo), 200
    
    return jsonify({'error': 'Cliente no encontrado'}), 404