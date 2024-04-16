from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from datetime import datetime
import json

from fastapi.responses import JSONResponse, StreamingResponse

from models.forca_model import Guess
from game_forca.game import GameForca
from utils.logger import logger

app = FastAPI()
game = GameForca()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    id = datetime.now().timestamp()
    logger.info(f"req_id={id} start request path={request.url.path}")
    response = await call_next(request)
    logger.info(f"req_id={id} completed request path={request.url.path} status_code={response.status_code}")
    return response

# TODO: Adicionar autenticação para esta rota.
@app.get("/logs", tags=["Logs"])
def get_logs():
    log_file = Path('logs/hangman_game.log')
    if not log_file.exists():
        return JSONResponse(status_code=404, content={"message": "Log file not found"})
    def log_streamer():
        log_file_path = Path('logs/hangman_game.log')
        with log_file_path.open(mode='rb') as log_file:
            yield from log_file
            
    return StreamingResponse(log_streamer(), media_type='text/plain')

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
