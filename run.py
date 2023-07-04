from llama_hub.web.sitemap.base import SitemapReader

# for jupyter notebooks uncomment the following two lines of code:
import nest_asyncio
nest_asyncio.apply()

loader = SitemapReader(html_to_text=True)
documents = loader.load_data(sitemap_url='https://deepshore.de/sitemap.xml', filter='https://deepshore.de/knowledge/2023-05-08')

documents = [documents.pop()]
print(len(documents))
print(documents[0].extra_info)

import os
from langchain.llms import GPT4All
#from gpt4all import GPT4All
from langchain.llms import LlamaCpp
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager

callbacks = [StreamingStdOutCallbackHandler()]
callback_manager = CallbackManager(callbacks)

local_path = "/Users/selamanse/Library/Application Support/nomic.ai/GPT4All"


#model_name = f"{os.getcwd()}/models/ggml-vicuna-13b-1.1-q4_2.bin"
#model_name = f"{os.getcwd()}/models/ggml-gpt4all-l13b-snoozy.bin"
#model_name = f"{os.getcwd()}/models/ggml-gpt4all-j-v1.3-groovy.bin"
#model_name = f"{os.getcwd()}/models/GPT4All-13B-snoozy.ggmlv3.q4_0.bin"
#model_name = f"{os.getcwd()}/models/open-llama-7B-open-instruct.ggmlv3.q4_0.bin"
model_name = f"{os.getcwd()}/models/open-llama-7B-open-instruct.ggmlv3.q6_K.bin"
#model_name = f"{local_path}/ggml-gpt4all-l13b-snoozy"

llm = LlamaCpp(model_path=model_name, callback_manager=callback_manager, verbose=True, use_mlock=False, n_gpu_layers=10000)

#llm = GPT4All(model="./models/ggml-gpt4all-l13b-snoozy", backend="gptj", callbacks=callbacks, verbose=True, n_ctx=2047, use_mlock=True, n_threads=8, f16_kv=False)
#llm = GPT4All(model_path=f"{os.getcwd()}/models", allow_download=False, model_name="ggml-gpt4all-j-v1.3-groovy.bin")
# import
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.embeddings.llamacpp import LlamaCppEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from llama_index.schema import Document

langchain_documents = []
for d in documents:
    langchain_documents.append(d.to_langchain_format())

# split it into chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(langchain_documents)

# create the open-source embedding function
#embedding_function = SentenceTransformerEmbeddings(model_name="./models/ggml-gpt4all-l13b-snoozy.bin")
embedding_function = LlamaCppEmbeddings(model_path=model_name, use_mlock=True, n_gpu_layers=1000, n_threads=8, n_ctx=2048, n_batch=500)

# load it into Chroma
db = Chroma.from_documents(docs, embedding_function)

# query it
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)

# print results
print(docs[0].page_content)