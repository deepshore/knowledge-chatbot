from contextlib import asynccontextmanager
from fastapi import FastAPI
import os
import logging
import sys
from llama_index import StorageContext, load_index_from_storage
from pydantic import BaseModel
from typing import Union
from llama_index.response.schema import Response

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

class DeepshoreChatRequest(BaseModel):
    question: str
    timestamp: Union[int, None] = None

class DeepshoreChatResponse(BaseModel):
    origin: Union[DeepshoreChatRequest, None] = None
    response: Union[str, None] = None
    related_articles: Union[list, None] = None
    error: Union[str, None] = None
    timestamp: Union[int, None] = None

# todo: put this into lifespan startup and add async tests
index = None

persist_dir = './storage' if (os.environ.get('PERSIST_DIR') == None) else os.environ.get('PERSIST_DIR')
storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
# load index
index = load_index_from_storage(storage_context)
print("PEEN")
if not index:
    raise Exception("Sorry, no numbers below zero")

# app start

app = FastAPI()

app.name = "Deepshore Chatbot API"

@app.get("/")
async def read_root():
    return {"message": "Deepshore Chatbot API"}

@app.post("/chatbot")
async def ask_chatbot(request: DeepshoreChatRequest):
    try:
        query_engine = index.as_query_engine()
        response = query_engine.query(request.question)

        related_articles = []
        for ex_i in response.metadata:
            related_articles.append(response.metadata[ex_i]['Source'])

        return {"answer": response.response,
                "related_articles": related_articles,
                "origin": request,
                "error": None,
                "timestamp": request.timestamp}

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return {"error": "An error occured"}
    
