import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vectorstore import get_vectorstore

def _load(path: str, filename: str):
    if filename.endswith('.pdf'):
        return PyPDFLoader(path).load()
    return TextLoader(path, encoding='utf-8').load()


def ingest_file(raw_bytes: bytes, filename: str):
    """Persist the file to a temp file, split it, embed it, store it."""
    suffix= os.path.splitext(filename)[1] or ".txt"
    with tempfile.NamedTemporaryFile(delete= False, suffix=suffix) as tmp:
        tmp.write(raw_bytes)
        tmp_path= tmp.name

        try:
            docs= _load(tmp_path, filename)
            print(f"DEBUG: Loaded {len(docs)} documents from {filename}")
            print(f"DEBUG: First doc content length: {len(docs[0].page_content)}")
            print(f"DEBUG: First doc content preview: {docs[0].page_content[:100]}")
            splitter= RecursiveCharacterTextSplitter(chunk_size= 1000, chunk_overlap= 200)
            chunks= splitter.split_documents(docs)
            print(f"DEBUG: Created {len(chunks)} chunks")
            for c in chunks:
                c.metadata['source']= filename
            
            get_vectorstore().add_documents(chunks)
            return len(chunks)

        finally:
            try:
                os.remove(tmp_path)
            except PermissionError:
                pass

