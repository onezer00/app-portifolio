from typing import Union
from fastapi import FastAPI
from datetime import datetime

from models.item_model import Item

app = FastAPI()

@app.get("/")
def read_root():
    return {"API Name": "FastAPI", "Time": datetime.now(), "Status": "Running"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}