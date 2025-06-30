# Imagen base
FROM python:3.10-slim

# Instalación de dependencias del sistema necesarias para WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libgobject-2.0-0 \
    libglib2.0-0 \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia todos los archivos
COPY . .

# Instala dependencias Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto (Fly.io usa 8080 por defecto)
EXPOSE 8080

# Comando para ejecutar la app (ajustado si usas Flask)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "run:app"]
