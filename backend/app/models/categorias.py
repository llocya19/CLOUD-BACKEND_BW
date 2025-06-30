# models/categorias.py

def get_all_categorias(cursor):
    cursor.execute("SELECT * FROM categorias ORDER BY id DESC")
    return cursor.fetchall()

def get_categoria_by_nombre(cursor, nombre):
    cursor.execute("SELECT id FROM categorias WHERE nombre = %s", (nombre,))
    return cursor.fetchone()

def get_categoria_by_id(cursor, id):
    cursor.execute("SELECT * FROM categorias WHERE id = %s", (id,))
    return cursor.fetchone()

def add_categoria(cursor, nombre, descripcion):
    cursor.execute("INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))

def update_categoria(cursor, id, nombre, descripcion):
    cursor.execute("UPDATE categorias SET nombre = %s, descripcion = %s WHERE id = %s", (nombre, descripcion, id))

def delete_categoria(cursor, id):
    cursor.execute("DELETE FROM categorias WHERE id = %s", (id,))
