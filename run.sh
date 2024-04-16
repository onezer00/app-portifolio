#!/bin/bash

# Nome do container Docker
CONTAINER_NAME="minha-aplicacao-fastapi"
# Nome da imagem Docker
IMAGE_NAME="minha-aplicacao-fastapi"

# Função para atualizar o repositório Git
update_repository() {
    echo "Atualizando repositório..."
    git pull origin main
    echo "Repositório atualizado."
}

# Função para parar e remover o container, se ele estiver rodando
stop_and_remove_container() {
    # Checa se o container existe
    if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
        echo "Parando e removendo o container existente..."
        # Força a remoção do container, mesmo que esteja rodando
        docker rm -f ${CONTAINER_NAME}
        echo "Container removido."
    else
        echo "Nenhum container existente para remover."
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

# Verifica se o diretório atual é um repositório Git
if git rev-parse --git-dir > /dev/null 2>&1; then
    update_repository
else
    echo "O diretório atual não é um repositório Git. Operação abortada."
    exit 1
fi

# Checa se o container já está rodando e atualiza se necessário
stop_and_remove_container
build_image
run_container

echo "Script concluído."
