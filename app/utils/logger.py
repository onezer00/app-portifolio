import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

def setup_logger():
    logger = logging.getLogger("hangman_game_logger")
    logger.setLevel(logging.INFO)  # Ajuste conforme a necessidade

    # Define um caminho relativo para o arquivo de log
    directory = Path.cwd() / 'logs'
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)

    # Define o caminho completo para o arquivo de log
    log_file_path = Path(directory / 'hangman_game.log')
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Cria um handler que escreve os logs para um arquivo, com rotação a cada 24 horas
    handler = TimedRotatingFileHandler(str(log_file_path ), when="midnight", interval=1, backupCount=3)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Chamada a função para configurar o logger quando o módulo é importado
logger = setup_logger()
