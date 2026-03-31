from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import QueryRequest, QueryResponse
from backend.app.services.rag_engine import RAGEngine
from backend.app.services.llm_service import LLMService

router = APIRouter()


@router.post("/generate", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    try:
        # 1. Initialize Engines
        rag = RAGEngine(request.subject)
        llm = LLMService()

        # 2. Retrieve & Generate
        context = rag.get_context(request.topic)
        answer = llm.generate_exam_notes(request.topic, context)

        return QueryResponse(status="success", answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))