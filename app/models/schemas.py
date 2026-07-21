from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str
    k: int

class SourceChunk(BaseModel):
    source: str
    snippet: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]

class UploadResponse(BaseModel):
    filename: str
    chunks_added: int
    