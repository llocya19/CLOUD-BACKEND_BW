from app import create_app
from flask import send_from_directory
import os

print("Inicializando app...")  # ✅ Log para saber si llega hasta aquí

app = create_app()
print("App creada correctamente")  # ✅ Verifica si create_app no falla

# Ruta raíz opcional pero útil (para verificar si el backend responde)
@app.route('/')
def index():
    return '🚀 Backend del SISTEMA_BW activo'

# Ruta para acceder a imágenes o archivos subidos
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Punto de entrada principal
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print(f"Ejecutando en puerto {port}...")  # ✅ Log útil
    app.run(host="0.0.0.0", port=port)
