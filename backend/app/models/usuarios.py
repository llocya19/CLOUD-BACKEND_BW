# backend/models/usuarios.py

def get_all_users(cursor):
    cursor.execute("""
        SELECT u.id, u.nombre, u.email, u.estado, u.foto,
        GROUP_CONCAT(r.nombre SEPARATOR ', ') AS roles
        FROM usuarios u
        LEFT JOIN usuarios_roles ur ON u.id = ur.usuario_id
        LEFT JOIN roles r ON ur.rol_id = r.id
        GROUP BY u.id ORDER BY u.id DESC
    """)
    return cursor.fetchall()

def get_user_by_email(cursor, email):
    cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
    return cursor.fetchone()

def get_user_by_id(cursor, id):
    cursor.execute("""
        SELECT id, nombre, email, estado, foto
        FROM usuarios
        WHERE id = %s
    """, (id,))
    return cursor.fetchone()

def add_user(cursor, nombre, email, contraseña, estado, foto):
    cursor.execute("""
        INSERT INTO usuarios (nombre, email, contraseña, estado, foto)
        VALUES (%s, %s, %s, %s, %s)
    """, (nombre, email, contraseña, estado, foto))

def update_user(cursor, id, nombre, email, estado, foto):
    cursor.execute("""
        UPDATE usuarios
        SET nombre = %s, email = %s, estado = %s, foto = %s
        WHERE id = %s
    """, (nombre, email, estado, foto, id))

def update_user_with_password(cursor, id, nombre, email, estado, foto, contraseña):
    cursor.execute("""
        UPDATE usuarios
        SET nombre = %s, email = %s, estado = %s, foto = %s, contraseña = %s
        WHERE id = %s
    """, (nombre, email, estado, foto, contraseña, id))

def delete_user(cursor, id):
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))

def asignar_roles(cursor, usuario_id, roles_ids):
    cursor.execute("DELETE FROM usuarios_roles WHERE usuario_id = %s", (usuario_id,))
    for rol_id in roles_ids:
        cursor.execute("""
            INSERT INTO usuarios_roles (usuario_id, rol_id)
            VALUES (%s, %s)
        """, (usuario_id, rol_id))

def get_roles(cursor):
    cursor.execute("SELECT id, nombre FROM roles ORDER BY nombre ASC")
    return cursor.fetchall()

def get_roles_por_usuario(cursor, usuario_id):
    cursor.execute("SELECT rol_id FROM usuarios_roles WHERE usuario_id = %s", (usuario_id,))
    return [r['rol_id'] for r in cursor.fetchall()]


def get_user_modules(cursor, user_id):
    cursor.execute("""
        SELECT m.nombre
        FROM modulos m
        JOIN roles_modulos rm ON m.id = rm.modulo_id
        JOIN usuarios_roles ur ON ur.rol_id = rm.rol_id
        WHERE ur.usuario_id = %s
    """, (user_id,))
    return cursor.fetchall()
