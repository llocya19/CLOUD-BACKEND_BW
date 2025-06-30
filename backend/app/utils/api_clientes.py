# backend/app/utils/api_clientes.py

import requests
from app.config import Config

API_TOKEN = Config.API_TOKEN
# Asegúrate que 'config.py' esté bien configurado

def consultar_dni_api(numero: str):
    try:
        if len(numero) == 8:
            url = f"https://api.apis.net.pe/v1/dni?numero={numero}"
        else:
            url = f"https://api.apis.net.pe/v1/ruc?numero={numero}"

        headers = {
            "Authorization": f"Bearer {API_TOKEN}"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if len(numero) == 8:
                return {
                    "nombre": f"{data.get('nombres', '')} {data.get('apellidoPaterno', '')} {data.get('apellidoMaterno', '')}".strip(),
                    "direccion": data.get("direccion", "")
                }
            else:
                return {
                    "nombre": data.get("nombre", ""),
                    "direccion": data.get("direccion", "")
                }
        else:
            print("Respuesta API:", response.status_code, response.text)
        return None

    except Exception as e:
        print("Error al consultar API externa:", e)
        return None
