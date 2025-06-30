# app/models/roles.py

def get_all_roles(cursor):
    """Obtiene todos los roles."""
    cursor.execute("SELECT id, nombre, descripcion FROM roles ORDER BY id DESC")
    return cursor.fetchall()

def get_role_by_name(cursor, nombre):
    """Obtiene un rol por su nombre."""
    cursor.execute("SELECT id FROM roles WHERE nombre = %s", (nombre,))
    return cursor.fetchone()

def add_role(cursor, nombre, descripcion):
    """Agrega un nuevo rol."""
    cursor.execute("INSERT INTO roles (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))

def update_role(cursor, id, nombre, descripcion):
    """Actualiza un rol existente."""
    cursor.execute("UPDATE roles SET nombre = %s, descripcion = %s WHERE id = %s", (nombre, descripcion, id))

def delete_role(cursor, id):
    """Elimina un rol."""
    cursor.execute("DELETE FROM roles WHERE id = %s", (id,))

def asignar_modulos_a_rol(cursor, rol_id, modulos):
    """Asigna módulos a un rol."""
    cursor.execute("DELETE FROM roles_modulos WHERE rol_id = %s", (rol_id,))
    for modulo_id in modulos:
        cursor.execute("INSERT INTO roles_modulos (rol_id, modulo_id) VALUES (%s, %s)", (rol_id, modulo_id))

def obtener_modulos_por_rol(cursor, rol_id):
    """Obtiene los módulos asignados a un rol."""
    cursor.execute("""
        SELECT m.id, m.nombre, m.ruta 
        FROM modulos m
        JOIN roles_modulos rm ON m.id = rm.modulo_id
        WHERE rm.rol_id = %s
    """, (rol_id,))
    return cursor.fetchall()

def get_all_modulos(cursor):
    """Obtiene todos los módulos disponibles."""
    cursor.execute("SELECT id, nombre, ruta FROM modulos ORDER BY id ASC")
    return cursor.fetchall()
