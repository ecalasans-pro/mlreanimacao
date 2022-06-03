from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

app = FastAPI()


class TaggedItem(BaseModel):
    name: str
    tags: Union[str, list]
    item_id: int


@app.get('/')
async def say_hello():
    return {'greeting': 'Olá, FastAPI'}


@app.get('/items/')
async def getItem(item: TaggedItem):
    return item


@app.get('/items/{item_id}')
async def getItems(item_id: int, count: int=1):
    return {'fetch': f"Fetched {count } of {item_id}"}
