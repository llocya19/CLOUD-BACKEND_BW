# Imagen base
FROM python:3.10-slim

# Instalación de dependencias del sistema necesarias para WeasyPrint y MySQL
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
    curl \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer puerto
EXPOSE 8080

# Comando para ejecutar la app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "run:app"]
