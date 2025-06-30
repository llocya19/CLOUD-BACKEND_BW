# backend/app/models/ventas.py

from datetime import datetime

def crear_venta(cursor, cliente_id, total, monto_pagado, cambio):
    cursor.execute("""
        INSERT INTO ventas (cliente_id, fecha_venta, total, monto_pagado, cambio)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        cliente_id,
        datetime.now(),
        total,
        monto_pagado,
        cambio
    ))
    return cursor.lastrowid

def insertar_detalle(cursor, venta_id, producto_id, cantidad, precio_unitario, subtotal):
    cursor.execute("""
        INSERT INTO detalle_venta 
        (venta_id, producto_id, cantidad, precio_unitario, subtotal)
        VALUES (%s, %s, %s, %s, %s)
    """, (venta_id, producto_id, cantidad, precio_unitario, subtotal))

def actualizar_stock(cursor, producto_id, cantidad_vendida):
    cursor.execute("""
        UPDATE productos
        SET cantidad_disponible = cantidad_disponible - %s
        WHERE id = %s
    """, (cantidad_vendida, producto_id))

def obtener_ventas(cursor):
    cursor.execute("""
        SELECT v.id, c.nombre AS cliente, v.fecha_venta, v.total 
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        ORDER BY v.fecha_venta DESC
    """)
    return cursor.fetchall()

def obtener_detalle(cursor, venta_id):
    cursor.execute("""
        SELECT v.id, c.nombre, c.dni, c.ruc, c.direccion,
               v.fecha_venta, v.total, v.monto_pagado, v.cambio
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        WHERE v.id = %s
    """, (venta_id,))
    venta = cursor.fetchone()

    cursor.execute("""
        SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.subtotal
        FROM detalle_venta dv
        JOIN productos p ON dv.producto_id = p.id
        WHERE dv.venta_id = %s
    """, (venta_id,))
    detalle = cursor.fetchall()

    return venta, detalle
