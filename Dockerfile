# Usar uma imagem base oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de requisitos primeiro, para aproveitar o cache de camadas do Docker
COPY requirements.txt ./

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia os demais arquivos do seu projeto
COPY ./app /app

# Informa ao Docker que a aplicação escuta na porta 8000
EXPOSE 8000

# Comando para executar a aplicação usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
