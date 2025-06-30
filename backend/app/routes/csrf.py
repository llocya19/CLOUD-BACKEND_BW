# backend/app/routes/csrf.py
from flask import Blueprint, jsonify
from flask_wtf.csrf import generate_csrf

csrf_bp = Blueprint('csrf', __name__)

@csrf_bp.route('/api/csrf-token', methods=['GET'])
def csrf_token():
    token = generate_csrf()
    return jsonify({'csrf_token': token})
