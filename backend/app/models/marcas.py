def get_all_marcas(cursor):
    cursor.execute("SELECT * FROM marcas ORDER BY id DESC")
    return cursor.fetchall()

def get_marca_by_nombre(cursor, nombre):
    cursor.execute("SELECT id FROM marcas WHERE nombre = %s", (nombre,))
    return cursor.fetchone()

def get_marca_by_id(cursor, id):
    cursor.execute("SELECT * FROM marcas WHERE id = %s", (id,))
    return cursor.fetchone()

def add_marca(cursor, nombre, descripcion):
    cursor.execute("INSERT INTO marcas (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))

def update_marca(cursor, id, nombre, descripcion):
    cursor.execute("UPDATE marcas SET nombre = %s, descripcion = %s WHERE id = %s", (nombre, descripcion, id))

def delete_marca(cursor, id):
    cursor.execute("DELETE FROM marcas WHERE id = %s", (id,))
