# backend/app/models/auth.py

def get_user_by_email(cursor, email):
    cursor.execute("""
        SELECT id, nombre, email, contraseña, estado, foto
        FROM usuarios
        WHERE email = %s
    """, (email,))
    return cursor.fetchone()

def get_roles_by_user(cursor, usuario_id):
    cursor.execute("""
        SELECT r.nombre FROM usuarios_roles ur
        JOIN roles r ON ur.rol_id = r.id
        WHERE ur.usuario_id = %s
    """, (usuario_id,))
    return [r['nombre'] for r in cursor.fetchall()]
# backend/app/models/usuarios.py

def get_user_modules(cursor, user_id):
    query = """
        SELECT m.id, m.nombre, m.ruta
        FROM modulos m
        INNER JOIN roles_modulos rm ON m.id = rm.modulo_id
        INNER JOIN usuarios_roles ur ON rm.rol_id = ur.rol_id
        WHERE ur.usuario_id = %s
        GROUP BY m.id, m.nombre, m.ruta
        ORDER BY m.id
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()
