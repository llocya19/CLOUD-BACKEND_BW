# backend/app/models/productos.py

def obtener_todos(cursor):
    cursor.execute("""
        SELECT 
            p.id, p.nombre, p.descripcion, p.precio_unitario, p.cantidad_disponible,
            p.imagen, p.codigo_barra, p.stock_inicial, p.fecha_ingreso,
            c.nombre AS categoria,
            m.nombre AS marca
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        LEFT JOIN marcas m ON p.marca_id = m.id
    """)
    return cursor.fetchall()

def obtener_por_id(cursor, producto_id):
    cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
    return cursor.fetchone()

def crear_producto(cursor, data):
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, precio_unitario, cantidad_disponible, imagen,
                               categoria_id, marca_id, codigo_barra, stock_inicial, fecha_ingreso)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['nombre'],
        data.get('descripcion'),
        data['precio_unitario'],
        data['cantidad_disponible'],
        data.get('imagen'),
        data.get('categoria_id'),
        data.get('marca_id'),
        data.get('codigo_barra'),
        data.get('stock_inicial'),
        data.get('fecha_ingreso')
    ))

def actualizar_producto(cursor, producto_id, data):
    cursor.execute("""
        UPDATE productos
        SET nombre = %s,
            descripcion = %s,
            precio_unitario = %s,
            cantidad_disponible = %s,
            imagen = %s,
            categoria_id = %s,
            marca_id = %s,
            codigo_barra = %s,
            stock_inicial = %s,
            fecha_ingreso = %s
        WHERE id = %s
    """, (
        data['nombre'],
        data.get('descripcion'),
        data['precio_unitario'],
        data['cantidad_disponible'],
        data.get('imagen'),
        data.get('categoria_id'),
        data.get('marca_id'),
        data.get('codigo_barra'),
        data.get('stock_inicial'),
        data.get('fecha_ingreso'),
        producto_id
    ))

def eliminar_producto(cursor, producto_id):
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
