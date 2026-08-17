import logging
from fastapi import APIRouter, HTTPException
from app.core.models import ChatRequest, ChatResponse, RetrievedSource
from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.prompt_service import build_prompt, is_relevant, NO_ANSWER_RESPONSE
from app.services.llm_service import call_llm

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
def health_check():
    """Basic health check endpoint."""
    return {"status": "ok"}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Main chat endpoint — accepts a question, returns a grounded answer."""
    
    question = request.question.strip()
    logger.info(f"Incoming question: {question}")
    
    # Validate input
    if not question:
        raise HTTPException(status_code=422, detail="Question cannot be empty")
    
    try:
        # Step 1: Retrieve relevant chunks
        chunks = retrieve_relevant_chunks(question)
        logger.info(f"Retrieved {len(chunks)} chunks: {[c['section_title'] for c in chunks]}")
        
        # Step 2: Check relevance — if weak, return no-answer
        if not is_relevant(chunks):
            logger.info("Chunks not relevant enough — returning no-answer response")
            return ChatResponse(
                answer=NO_ANSWER_RESPONSE,
                sources=[],
                retrieved_chunks_count=len(chunks)
            )
        
        
        # Step 3: Build prompt
        messages = build_prompt(question, chunks)
        
        # Step 4: Call LLM
        answer = call_llm(messages)
        
        # Step 5: Format sources
        sources = [
            RetrievedSource(
                chunk_id=c["chunk_id"],
                section_title=c["section_title"],
                source_file=c["source_file"]
            )
            for c in chunks
        ]
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            retrieved_chunks_count=len(chunks)
        )
    
    except RuntimeError as e:
        logger.error(f"Runtime error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")