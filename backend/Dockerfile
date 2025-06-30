# Imagen base oficial de Python
FROM python:3.11-slim

# Instala dependencias necesarias para mysqlclient y WeasyPrint
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
    default-libmysqlclient-dev \
    libmysqlclient-dev \
    pkg-config \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia todos los archivos del proyecto
COPY . .

# Actualiza pip e instala las dependencias Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto (Fly.io espera 8080)
EXPOSE 8080

# Comando para ejecutar la app con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "run:app"]
