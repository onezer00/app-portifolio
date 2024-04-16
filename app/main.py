from fastapi import FastAPI, HTTPException
from datetime import datetime
import json

from fastapi.responses import JSONResponse

from models.forca_model import Guess
from game_forca.game import GameForca

app = FastAPI()
game = GameForca()

@app.get("/", tags=["Health Check"])
def read_root():
    return {"API Name": "FastAPI", "Time": datetime.now(), "Status": "Running"}

@app.post("/guess", tags=["Game Forca"])
def make_guess(guess: Guess):
    if game.chances <= 0 or not game.palavra:
        game.end_game()
        content = {"message": "Sorry, you dont won! Try again.", "status": "The game not started", "action": "Try access '/start' to start the game"}
        return JSONResponse(status_code=404, content=content)
    
    result = game.input_letra(guess.letter.upper())
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    if '_' not in game.lista:
        result.update({"message": "Congratulations, you won!", "status": "won"})
        game.end_game()
    return result

@app.get("/start", tags=["Game Forca"])
def start_game():
    return game.start_game()
