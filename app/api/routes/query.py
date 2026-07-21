from fastapi import APIRouter
from app.models.schemas import QueryRequest, QueryResponse, SourceChunk
from app.services.rag import answer_question, stream_answer
from fastapi.responses import StreamingResponse

router= APIRouter(tags=["query"])

@router.post("/", response_model=QueryResponse)
async def query_documents(query: QueryRequest):
    answer, sources = answer_question(query.query, query.k)
    return QueryResponse(
        answer=answer, 
        sources=[SourceChunk(**s) for s in sources],
        )


@router.post("/query/stream")
async def query_stream(req: QueryRequest):
    generator= stream_answer(req.query, req.k)
    return StreamingResponse(generator, media_type="text/plain")

