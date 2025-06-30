# Imagen base oficial
FROM python:3.10-slim

# Instala dependencias del sistema necesarias para:
# - mysqlclient (default-libmysqlclient-dev, libmysqlclient-dev, pkg-config)
# - WeasyPrint (renderizado PDF y dependencias gráficas)
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
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia todo el proyecto
COPY . .

# Instala dependencias Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto usado por Fly.io
EXPOSE 8080

# Ejecuta la app Flask con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "run:app"]
