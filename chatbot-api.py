from fastapi import FastAPI
import os
import logging
import sys
from llama_index import StorageContext, load_index_from_storage
from pydantic import BaseModel
from typing import Union

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

app = FastAPI()

app.name = "Deepshore Chatbot API"

index = None

class DeepshoreChatRequest(BaseModel):
    question: str
    timestamp: Union[int, None] = None

class DeepshoreChatResponse(BaseModel):
    origin: Union[DeepshoreChatRequest, None] = None
    response: Union[str, None] = None
    related_articles: Union[list, None] = None
    error: Union[str, None] = None
    timestamp: Union[int, None] = None

def load_index():
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    # load and return index
    return load_index_from_storage(storage_context)

@app.get("/")
async def read_root():
    return {"message": "Deepshore Chatbot API"}

@app.post("/chatbot")
async def ask_chatbot(request: DeepshoreChatRequest):
    try:
        query_engine = index.as_query_engine()
        response = query_engine.query(request.question)

        related_articles = []
        for ex_i in response.extra_info:
            related_articles.append(response.extra_info[ex_i]["Source"])

        return {"answer": response.response,
                "related_articles": related_articles,
                "origin": request,
                "error": None,

                "timestamp": request.timestamp}
    except:
        return {"error": "An error occured"}
    


index = load_index()