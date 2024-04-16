#!/bin/bash

# Nome do container Docker
CONTAINER_NAME="minha-aplicacao-fastapi"
# Nome da imagem Docker
IMAGE_NAME="minha-aplicacao-fastapi"

# Função para criar um arquivo de log
create_log_file() {
    # Cria um arquivo de log com a data e hora atual
    LOG_FILE="logs/hangman_game.log"
    touch ${LOG_FILE}
    echo "Dando permissões de escrita e leitura ao arquivo de log..."
    chmod 666 ${LOG_FILE}
    echo "Arquivo de log criado: ${LOG_FILE}"
}

# Função para atualizar o repositório Git
update_repository() {
    echo "Atualizando repositório..."
    # Stash quaisquer mudanças que o script possa ter causado
    git stash --include-untracked
    # Puxe as últimas mudanças do repositório
    git pull origin main
    # Aplica o stash, mas não restaure o arquivo de script (run_container.sh)
    git stash apply --exclude=run_container.sh
    # Verifica se o script atual foi modificado após o git pull
    if [ -n "$(git diff --name-only HEAD@{1} run_container.sh)" ]; then
        echo "O script foi atualizado... Reiniciando o script."
        exec $0
        exit
    fi
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

# Função para rodar o container e acompanhar os logs
run_container_and_follow_logs() {
    echo "Levantando o novo container..."
    docker run -p 8000:8000 --name ${CONTAINER_NAME} ${IMAGE_NAME}
    # O comando acima irá manter o container em primeiro plano e mostrar os logs diretamente
}

# Verifica se o diretório atual é um repositório Git
if git rev-parse --git-dir > /dev/null 2>&1; then
    update_repository
else
    echo "O diretório atual não é um repositório Git. Operação abortada."
    exit 1
fi

# Checa se o container já está rodando e atualiza se necessário
create_log_file
stop_and_remove_container
build_image
run_container_and_follow_logs

echo "Script concluído."
