def actualizar_empresa(cursor, data):
    cursor.execute("""
        UPDATE empresa SET
            nombre_comercial = %s,
            ruc = %s,
            direccion = %s,
            telefono = %s,
            correo = %s,
            web = %s,
            logo = %s
        WHERE id = 1
    """, (
        data['nombre_comercial'],  # 👈 CORREGIDO
        data['ruc'],
        data['direccion'],
        data['telefono'],
        data['correo'],
        data['web'],
        data['logo']
    ))
def obtener_empresa(cursor):
    cursor.execute("SELECT * FROM empresa WHERE id = 1")
    return cursor.fetchone()
