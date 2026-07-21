from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import UploadResponse
from app.services.ingest import ingest_file

router= APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model= UploadResponse)
async def upload_document(file: UploadFile= File(...)):
    allowed= (".pdf", ".txt", ".md")
    if not file.filename.lower().endswith(allowed):
        raise HTTPException(status_code= 400, detail= f"File type not allowed. Allowed types: {allowed}")
    raw= await file.read()
    chunks= ingest_file(raw, file.filename)
    return UploadResponse(filename= file.filename, chunks_added= chunks)

