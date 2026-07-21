from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings

_embeddings= OllamaEmbeddings(model=settings.embed_model, base_url=settings.ollama_base_url)
_vectorstore= Chroma(
    collection_name="documents",
    embedding_function=_embeddings,
    persist_directory=settings.chroma_dir
)

def get_vectorstore():
    return _vectorstore
