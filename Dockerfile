# Imagen base
FROM python:3.11-slim

# Variables de entorno para evitar buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Copia dependencias e instala
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY backend/ .

# Expone el puerto
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "app.py"]
