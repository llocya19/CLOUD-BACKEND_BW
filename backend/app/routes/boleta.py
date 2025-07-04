# backend/app/routes/boleta.py

from flask import Blueprint, render_template, make_response, request
from app.database import get_db
from app.models import ventas as modelo_ventas
from app.models import empresa as modelo_empresa
from weasyprint import HTML
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import os
import sys
from app.extensions import cache
boleta_bp = Blueprint('boleta', __name__)

@boleta_bp.route('/api/ventas/<int:id>/boleta', methods=['GET'])
@cache.cached(timeout=120)
def generar_boleta(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Obtener venta y detalle
    venta, detalle = modelo_ventas.obtener_detalle(cursor, id)
    if not venta:
        return {'error': 'Venta no encontrada'}, 404

    empresa = modelo_empresa.obtener_empresa(cursor)

    # Manejo del logo
    logo_url = None
    if empresa and empresa.get('logo'):
        ruta_logo = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', 'uploads', empresa['logo'])
        )
        print("🖼️ Ruta logo absoluta:", ruta_logo, file=sys.stderr)
        if os.path.exists(ruta_logo):
            logo_url = f'file://{ruta_logo}'  # ✅ Necesario para que WeasyPrint lea el archivo
        else:
            print("❌ Logo no encontrado:", ruta_logo, file=sys.stderr)

    # Convertir fecha UTC naive a Lima
    if isinstance(venta['fecha_venta'], datetime) and venta['fecha_venta'].tzinfo is None:
        venta['fecha_venta'] = venta['fecha_venta'].replace(tzinfo=timezone.utc).astimezone(ZoneInfo('America/Lima'))

    # Totales
    venta['total'] = float(venta['total'])
    venta['monto_pagado'] = float(venta['monto_pagado'])
    venta['cambio'] = float(venta['cambio'])

    # Letras
    total_letras = f"{venta['total']:.2f}".replace('.', ' SOLES CON ') + " CENTIMOS"

    # Render HTML
    html = render_template(
        'boleta.html',
        empresa=empresa,
        venta=venta,
        productos=detalle,
        total_letras=total_letras,
        logo_url=logo_url
    )

    # ✅ Base_url = cwd para acceso a archivos locales
    pdf = HTML(string=html, base_url=os.getcwd()).write_pdf()

    # Respuesta
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=boleta_{id}.pdf'
    return response