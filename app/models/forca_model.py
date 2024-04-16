from pydantic import BaseModel

class Guess(BaseModel):
    letter: str