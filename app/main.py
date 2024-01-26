from fastapi import FastAPI, status
import os
import logging
import sys
from llama_index import StorageContext, ServiceContext, load_index_from_storage, set_global_service_context, VectorStoreIndex
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding
from llama_index.embeddings.openai import OpenAIEmbeddingMode, OpenAIEmbeddingModelType
from pydantic import BaseModel
from typing import Union
from llama_hub.web.sitemap.base import SitemapReader

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

llm = OpenAI(model="gpt-3.5-turbo")
embed_model = OpenAIEmbedding(mode=OpenAIEmbeddingMode.TEXT_SEARCH_MODE, model=OpenAIEmbeddingModelType.TEXT_EMBED_ADA_002)
service_context = ServiceContext.from_defaults(llm=llm,
                                               embed_model=embed_model)
set_global_service_context(service_context=service_context)

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

def refresh_index():
    global index
    print("refresh_index")
    loader = SitemapReader(html_to_text=True)
    documents = loader.load_data(sitemap_url='https://deepshore.de/sitemap.xml', filter='https://deepshore.de/knowledge')
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist()

try:
    persist_dir = './storage' if (os.environ.get('PERSIST_DIR') == None) else os.environ.get('PERSIST_DIR')
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    # load index
    index = load_index_from_storage(storage_context)
except Exception as err:
    print(err)
    refresh_index()

if not index:
    raise Exception("Sorry, no numbers below zero")

# app start
app = FastAPI()
app.name = "Deepshore Chatbot API"

@app.get("/")
async def read_root():
    return {"message": "Deepshore Chatbot API"}

@app.put("/refresh-index", status_code=status.HTTP_204_NO_CONTENT)
async def get_refresh_index():
    global index
    refresh_index()

@app.post("/chatbot")
async def ask_chatbot(request: DeepshoreChatRequest):
    global index
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
    
