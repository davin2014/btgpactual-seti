# Despliegue de Frontend y Backend con CloudFormation

## Requisitos

- AWS CLI configurado
- AWS CloudFormation
- Docker (para construir la imagen de FastAPI)
- AWS ECR (para almacenar la imagen de Docker)

## Pasos para el Despliegue

### 1. Despliegue del Frontend (React)

1. Navega al directorio `cloudformation`.
2. Ejecuta el siguiente comando para crear el stack de CloudFormation para el frontend:

   ```sh
   aws cloudformation create-stack --stack-name react-app-stack --template-body file://frontend.yaml