# backend/app/utils/otp.py
import random
from app.extensions import mail

from datetime import datetime, timedelta
from flask_mail import Message
from app import mail
from app.database import get_db

def generar_otp():
    return str(random.randint(100000, 999999))

def enviar_otp_por_correo(email, nombre, otp):
    msg = Message('Código de Verificación - Sistema',
                  sender='tucorreo@gmail.com',
                  recipients=[email])
    msg.body = f"Hola {nombre}, tu código OTP es: {otp}. Tiene 5 minutos de validez."
    mail.send(msg)

def crear_y_enviar_otp(usuario_id, email, nombre):
    db = get_db()
    cursor = db.cursor()

    otp = generar_otp()
    expires_at = datetime.now() + timedelta(minutes=5)

    cursor.execute("INSERT INTO otps (usuario_id, otp, expires_at) VALUES (%s, %s, %s)",
                   (usuario_id, otp, expires_at))
    db.commit()

    enviar_otp_por_correo(email, nombre, otp)
