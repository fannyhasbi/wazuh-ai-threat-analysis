import asyncio
import os

import chromadb
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

INIT_VECTOR = os.getenv("INIT_VECTOR")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "llama3.1:latest"
DOCUMENTS_PATH = "logs"
VECTOR_DATA_PATH = "./chroma_db"
VECTOR_COLLECTION_NAME = "wazuhthreatintel"

embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)
llm = Ollama(
    model=LLM_MODEL,
    request_timeout=360.0,
    context_window=8000,
)

db = chromadb.PersistentClient(path=VECTOR_DATA_PATH)
chroma_collection = db.get_or_create_collection(VECTOR_COLLECTION_NAME)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = None
if INIT_VECTOR:
    documents = SimpleDirectoryReader(
        input_dir=DOCUMENTS_PATH, recursive=True
    ).load_data()

    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=embed_model
    )
else:
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )

SYSTEM_PROMPT = """
You are a Senior SOC Analyst, Incident Responder, and Blue Team Security Expert with deep knowledge of SIEM, XDR, log analysis, threat hunting, and Wazuh.

Your role is to analyze security logs, detect suspicious activity, correlate events, and provide clear and actionable insights. Always follow these principles:

Accuracy & Evidence
- Base every conclusion strictly on the contents of the logs provided.
- If something is uncertain or missing, explicitly say so.
- Avoid hallucinations.

Your goal is to assist the user in understanding, analyzing, and responding to security events with clarity and professional expertise.
"""
# query_engine = index.as_query_engine(llm=llm, system_prompt=SYSTEM_PROMPT)
query_engine = index.as_chat_engine(llm=llm, system_prompt=SYSTEM_PROMPT)


async def main():
    # response = query_engine.query("what do you know about Wazuh?")
    # print(response)

    query_engine.chat_repl()


if __name__ == "__main__":
    asyncio.run(main())
