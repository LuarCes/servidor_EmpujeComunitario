# Usamos una imagen ligera de Python
FROM python:3.10-slim

# Directorio de trabajo
WORKDIR /app

# Instalamos dependencias del sistema para compilar si es necesario
RUN apt-get update && apt-get install -y protobuf-compiler && rm -rf /var/lib/apt/lists/*

# Copiamos los archivos de requisitos e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código y el archivo .proto
COPY . .

# Compilamos el archivo proto para generar los stubs de Python
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ong.proto

# Puerto que usa gRPC (por defecto suele ser 50051)
EXPOSE 50051

# Comando para arrancar el servidor
CMD ["python", "server.py"]