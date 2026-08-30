from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class PriorityEnum(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class ActionItem(BaseModel):
    task: str = Field(description="Clear, actionable task description")
    assignee: str = Field(description="Name of person assigned, or 'Unassigned'")
    priority: PriorityEnum = Field(description="Task urgency priority level")

class TextAnalysisResponse(BaseModel):
    summary: str = Field(description="Concise 2-sentence executive summary")
    key_topics: List[str] = Field(description="List of primary topics discussed")
    action_items: List[ActionItem] = Field(description="Extracted list of actionable tasks")
    risk_score: float = Field(description="Assessed risk score from 0.0 (low) to 1.0 (critical)")

class IngestDocumentRequest(BaseModel):
    document_id: str = Field(description="Unique identifier for the document (e.g ., doc_101)")
    title: str = Field(description="Title of the document")
    content: str = Field(description="Content of the document")
    metadata: Optional[Dict[str, Any]] = Field(description="Additional metadata about the document (e.g., department,author)")

class IngestResponse(BaseModel):
    document_id:str
    total_chunks:int   
    message: str 
    provider_used: str

class SearchRequest(BaseModel):
    query: str=Field(description="Natural language Search query string")
    top_k: int=Field(default=3, description="Number of top results to return")
    filter_metadata: Optional[Dict[str, Any]]= Field(
        default=None,
        description="Optional metadata filters e.g. {'department':'IT'}"
    )
class SearchResultItem(BaseModel):
    chunk_id:str
    document_id:str
    text:str
    score:float = Field(description=" Cosine distance or similarity score - Relevance score from 0.0 to 1.0")
    metadata=Dict[str, Any]

class SearchResponse(BaseModel):
    query:str
    results:List[SearchResultItem]
    provider_used: str

class SystemStatusResponse(BaseModel):
    embedding_provider: str
    collection_name: str
    total_indexed_chunks: int
