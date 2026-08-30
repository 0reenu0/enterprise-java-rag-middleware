from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from schemas import (
    TextAnalysisResponse,
    IngestDocumentRequest, IngestResponse,
    SearchRequest,SearchResponse)
from llm_service import LLMService
from chunking import DocumentChunker
from vector_store import VectorStoreService

app = FastAPI(title="Enterprise GenAI Engine - Day 3")
llm_service = LLMService()
chunker=DocumentChunker(chunk_size=200,chunk_overlap=40)
vector_store=VectorStoreService()

class AnalysisRequest(BaseModel):
    raw_text: str

@app.post("/api/v1/analyze", response_model=TextAnalysisResponse)
async def analyze_text(request: AnalysisRequest):
    if not request.raw_text.strip():
        raise HTTPException(status_code=400, detail="raw_text cannot be empty")

    try:
        result = llm_service.parse_unstructured_text(request.raw_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/ingest", response_model=IngestResponse)
async def ingest_document(request: IngestDocumentRequest):
    if not request.content.strip():
        raise HTTPException(status_code=400, detail="Document content cannot be empty !")

    try:
        chunks=chunker.split_text(
            text=request.content,
            doc_id=request.document_id,
            title=request.title,
            extra_metadata=request.metadata
        )
        inserted_count= vector_store.add_chunks(chunks)

        return IngestResponse(
            document_id=request.document_id,
            total_chunks=inserted_count,
            provider_used=vector_store.provider,
            message=f"Successfully indexed {inserted_count} chunks into ChromaDB using '{vector_store.provider}' provider!"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/search", response_model=SearchResponse)
async def search_vector_store(request:SearchRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be mepty")

    try:
        results= vector_store.search(query=request.query, 
        top_k=request.top_k,
        filter_metadata==request.filter_metadata
        )
        return SearchResponse(query=request.query, 
        provider_used=vector_store.provider,
        results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/api/v1/status", response_model=SystemStatusResponse)
async def get_system_status():
    return SystemStatusResponse(
        embedding_provider=vector_store.provider,
        collection_name=vector_store.collection_name,
        total_indexed_chunks=vector_store.count()
    )
