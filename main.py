from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from schemas import TextAnalysisResponse
from llm_service import LLMService

app = FastAPI(title="Enterprise GenAI Engine - Day 1")
llm_service = LLMService()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)