# Usa la imagen oficial de Python 3.11 slim
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia las dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto
COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["python", "main.py"]