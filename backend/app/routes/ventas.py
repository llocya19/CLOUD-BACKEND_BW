# backend/app/routes/ventas.py

from flask import Blueprint, request, jsonify
from app.database import get_db
from app.models import ventas as modelo
from app.models import clientes
from datetime import datetime
from app.utils.api_clientes import consultar_dni_api
from flask import render_template, make_response
from weasyprint import HTML
import io
from app.models import empresa as modelo_empresa
from app.extensions import cache

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/api/ventas', methods=['POST'])
def registrar_venta():
    db = get_db()
    cursor = db.cursor()

    datos = request.get_json()
    cliente_info = datos.get('cliente')
    productos = datos.get('productos')
    monto_pagado = float(datos.get('monto_pagado', 0))

    if not cliente_info or not productos:
        return jsonify({'error': 'Datos incompletos'}), 400

    dni_ruc = cliente_info.get('dni') or cliente_info.get('ruc')
    tipo_cliente = 'persona' if len(dni_ruc) == 8 else 'empresa'

    cursor.execute("SELECT id FROM clientes WHERE dni = %s OR ruc = %s", (dni_ruc, dni_ruc))
    cliente = cursor.fetchone()

    if cliente:
        cliente_id = cliente[0]
    else:
        # Buscar en la API externa
        datos_api = consultar_dni_api(dni_ruc)
        nombre = cliente_info.get('nombre', '')
        direccion = cliente_info.get('direccion', '')

        # Si API devuelve datos, actualizar nombre y dirección
        if datos_api:
            if 'nombre' in datos_api:
                nombre = datos_api['nombre']
            if 'direccion' in datos_api and datos_api['direccion']:
                direccion = datos_api['direccion']
            # Si la API no da dirección, usamos la ingresada manualmente

        # Insertar nuevo cliente
        if tipo_cliente == 'persona':
            cursor.execute("""
                INSERT INTO clientes (nombre, dni, tipo_cliente, direccion)
                VALUES (%s, %s, %s, %s)
            """, (nombre, dni_ruc, tipo_cliente, direccion))
        else:
            cursor.execute("""
                INSERT INTO clientes (nombre, ruc, tipo_cliente, direccion)
                VALUES (%s, %s, %s, %s)
            """, (nombre, dni_ruc, tipo_cliente, direccion))
        
        cliente_id = cursor.lastrowid

    # Validar stock y calcular total
    subtotal = 0
    for p in productos:
        precio = float(p['precio_unitario'])
        cantidad = int(p['cantidad'])

        cursor.execute("SELECT nombre, cantidad_disponible FROM productos WHERE id = %s", (p['id'],))
        prod = cursor.fetchone()
        if not prod or prod[1] < cantidad:
            return jsonify({'error': f"Stock insuficiente para producto {prod[0]}"}), 400

        subtotal += precio * cantidad

    igv = round(subtotal * 0.18, 2)
    total = round(subtotal + igv, 2)
    cambio = round(monto_pagado - total, 2)

    if monto_pagado < total:
        return jsonify({'error': 'El monto pagado es insuficiente'}), 400

    try:
        venta_id = modelo.crear_venta(cursor, cliente_id, total, monto_pagado, cambio)

        for p in productos:
            precio = float(p['precio_unitario'])
            cantidad = int(p['cantidad'])
            sub = precio * cantidad
            modelo.insertar_detalle(cursor, venta_id, p['id'], cantidad, precio, sub)
            modelo.actualizar_stock(cursor, p['id'], cantidad)

        db.commit()
        return jsonify({'mensaje': 'Venta registrada', 'venta_id': venta_id}), 201

    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500


@ventas_bp.route('/api/ventas', methods=['GET'])
@cache.cached(timeout=60) 
def listar_ventas():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
        v.id, 
            DATE_FORMAT(v.fecha_venta, '%Y-%m-%d %H:%i:%s') AS fecha_venta,

        v.total, 
        c.nombre, 
        c.dni
    FROM ventas v
    JOIN clientes c ON v.cliente_id = c.id
    ORDER BY v.fecha_venta DESC
    """)

    ventas = cursor.fetchall()

    return jsonify(ventas), 200



@ventas_bp.route('/api/ventas/<int:id>', methods=['GET'])
@cache.cached(timeout=60) 
def detalle_venta(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    venta, detalle = modelo.obtener_detalle(cursor, id)

    if not venta:
        return jsonify({'error': 'Venta no encontrada'}), 404

    # Conversión segura de números
    venta['total'] = float(venta['total'])
    venta['monto_pagado'] = float(venta['monto_pagado'])
    venta['cambio'] = float(venta['cambio'])

    # ✅ Convertir fecha_venta a string con hora local (no UTC)
    if isinstance(venta['fecha_venta'], datetime):
        venta['fecha_venta'] = venta['fecha_venta'].strftime('%Y-%m-%d %H:%M:%S')

    for item in detalle:
        item['precio_unitario'] = float(item['precio_unitario'])
        item['subtotal'] = float(item['subtotal'])

    return jsonify({
        'id': venta['id'],
        'fecha_venta': venta['fecha_venta'],  # ✅ ya convertida como string
        'cliente': {
            'nombre': venta['nombre'],
            'direccion': venta['direccion']
        },
        'productos': detalle,
        'total': venta['total'],
        'monto_pagado': venta['monto_pagado'],
        'cambio': venta['cambio']
    }), 200

