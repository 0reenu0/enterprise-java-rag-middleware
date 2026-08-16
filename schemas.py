from enum import Enum
from typing import List
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
