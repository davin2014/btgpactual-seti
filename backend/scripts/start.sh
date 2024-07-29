#!/bin/bash
# Crear el directorio para los datos de MongoDB si no existe
mkdir -p ./data/db
# Construir los contenedores
docker-compose build
# Levantar los contenedores
docker-compose up -d
# Esperar a que los contenedores estén listos
sleep 10
# Ejecutar el script de inicialización
#docker-compose exec app_container python initialize_db.py