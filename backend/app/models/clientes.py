# backend/app/models/clientes.py

def obtener_todos(cursor):
    cursor.execute("""
        SELECT id, nombre, email, telefono, direccion, dni, ruc, tipo_cliente
        FROM clientes
    """)
    return cursor.fetchall()

def obtener_por_id(cursor, cliente_id):
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente_id,))
    return cursor.fetchone()

def crear_cliente(cursor, data):
    cursor.execute("""
        INSERT INTO clientes (nombre, email, telefono, direccion, dni, ruc, tipo_cliente)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data['nombre'],
        data['email'],
        data['telefono'],
        data['direccion'],
        data['dni'],
        data.get('ruc', ''),
        data['tipo_cliente']
    ))

def actualizar_cliente(cursor, cliente_id, data):
    cursor.execute("""
        UPDATE clientes
        SET nombre = %s,
            email = %s,
            telefono = %s,
            direccion = %s,
            dni = %s,
            ruc = %s,
            tipo_cliente = %s
        WHERE id = %s
    """, (
        data['nombre'],
        data['email'],
        data['telefono'],
        data['direccion'],
        data['dni'],
        data.get('ruc', ''),
        data['tipo_cliente'],
        cliente_id
    ))

def eliminar_cliente(cursor, cliente_id):
    cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
