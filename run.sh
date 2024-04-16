#!/bin/bash

# Nome do container Docker
CONTAINER_NAME="minha-aplicacao-fastapi"
# Nome da imagem Docker
IMAGE_NAME="minha-aplicacao-fastapi"

# Função para parar e remover o container, se ele estiver rodando
stop_and_remove_container() {
  if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    echo "Parando e removendo o container existente..."
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
    echo "Container removido."
  fi
}

# Função para construir a imagem Docker
build_image() {
  echo "Construindo a imagem Docker..."
  docker build -t ${IMAGE_NAME} .
  echo "Imagem construída."
}

# Função para rodar o container
run_container() {
  echo "Levantando o novo container..."
  docker run -d -p 8000:8000 --name ${CONTAINER_NAME} ${IMAGE_NAME}
  echo "Container rodando."
}

# Checa se o container já está rodando e atualiza se necessário
stop_and_remove_container
build_image
run_container

echo "Script concluído."
