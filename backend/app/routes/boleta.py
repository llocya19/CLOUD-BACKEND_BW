# backend/app/routes/boleta.py

from flask import Blueprint, render_template, make_response, request, url_for
from app.database import get_db
from app.models import ventas as modelo_ventas
from app.models import empresa as modelo_empresa
from weasyprint import HTML
import os

boleta_bp = Blueprint('boleta', __name__)

@boleta_bp.route('/api/ventas/<int:id>/boleta', methods=['GET'])
def generar_boleta(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Obtener venta y productos
    venta, detalle = modelo_ventas.obtener_detalle(cursor, id)
    if not venta:
        return {'error': 'Venta no encontrada'}, 404

    # Obtener empresa
    empresa = modelo_empresa.obtener_empresa(cursor)

    # Ruta del logo
    logo_url = None
    if empresa and empresa.get('logo'):
        logo_url = url_for('uploaded_file', filename=empresa['logo'], _external=True)

    # Calcular texto total en letras
    total_letras = f"{venta['total']:.2f}".replace('.', ' con ') + " SOLES"
    venta['total'] = float(venta['total'])
    venta['monto_pagado'] = float(venta['monto_pagado'])
    venta['cambio'] = float(venta['cambio'])


    # Renderizar HTML
    html = render_template(
        'boleta.html',
        empresa=empresa,
        venta=venta,
        productos=detalle,  # ✅ nombre correcto para el for
        total_letras=total_letras,
        logo_url=logo_url
    )

    # Convertir a PDF
    pdf = HTML(string=html, base_url=request.host_url).write_pdf()

    # Respuesta
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename=boleta_{id}.pdf'
    return response
