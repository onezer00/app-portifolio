"""
Este programa foi desenvolvido por Oner
Jogo de forca criado em python
Considere que o programa esta em desenvolvimento
Considere deixar uma estrela no git se esse programa foi útil para você
"""
import unicodedata

import requests
import json

class GameForca:
    """
    Classe GameForca
    """

    def __init__(self):
        self.palavra = None
        self.tamanho = None
        self.acertos = 0
        self.chances = 6
        self.lista = []

    def get_palavra(self):
        """
        Retorna uma palavra aleatória da API de dicionário
        Atribui a palavra e tamanho ao objeto
        """
        url = 'https://api.dicionario-aberto.net/random'

        response = requests.get(url)

        self.palavra = ''.join(
            ch
            for ch in unicodedata.normalize('NFKD', response.json()['word'])
            if not unicodedata.combining(ch)
        ).upper()
        self.tamanho = len(self.palavra)
        return {"word": self.palavra, "length": self.tamanho}

    def get_letra(self, letra):
        """
        Verifica se a letra já foi digitada e retorna True ou False
        """
        if len(letra) > 1 or letra not in self.palavra:
            self.chances -= 1
            return {"error": "Incorrect or more than one letter entered", "remaining_chances": self.chances}
        self.acertos += 1
        return {"success": "Correct letter", "remaining_chances": self.chances}

    def input_letra(self, letra):
        """
        Verifica se a letra já foi digitada e retorna a letra ou um erro
        """
        if letra in self.lista:
            return {"error": "Letter already entered"}
        result = self.get_letra(letra)
        if result.get("success"):
            self.lista = [
                letra if letra == self.palavra[i] else self.lista[i]
                for i in range(self.tamanho)
            ]
            return {
                "letter": letra,
                "current_state": self.lista,
                "remaining_chances": self.chances
            }
        return result

    # pylint: disable=expression-not-assigned
    def start_game(self):
        """
        Inicializa o jogo
        """
        palavra_info = self.get_palavra()
        self.lista = ['_' for _ in range(self.tamanho)]
        self.acertos = 0
        self.chances = 6

        return {
            "message": "Starting Hangman Game",
            "word_info": palavra_info,
            "status": "in_progress",
            "remaining_chances": self.chances,
            "current_state": self.lista
        }
        
    def end_game(self):
        """
        Finalizando o jogo no caso de vitória ou derrota
        """
        self.palavra = None
        self.tamanho = None
        self.acertos = 0
        self.chances = 6
        self.lista = []
        
        
