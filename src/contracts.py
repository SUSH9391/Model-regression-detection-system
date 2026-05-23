from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field

class EmailAnalysis(BaseModel):
    category: Literal["billing", "technical", "account", "general"]
    summary: str

class PromptConfig(BaseModel):
    version_id: str
    timestamp: datetime
    system_prompt: str
    model: str = "gpt-4o-mini"
    temperature: float = 0.0

class TestCase(BaseModel):
    id: str
    input_text: str
    expected_category: str
    expected_summary: Optional[str] = None
    expected_difficulty: Literal["easy", "medium", "hard"]
    notes: str = ""

class EvalResult(BaseModel):
    test_case_id: str
    status: Literal["success", "failed"]
    output: Optional[dict] = None
    error: Optional[str] = None
    metrics: dict[str, float | int] = Field(
        default_factory=lambda: {"category_match": 0.0, "latency": 0.0, "tokens_used": 0}
    )

class RunSummary(BaseModel):
    run_id: str
    prompt_version: str
    model: str
    timestamp: datetime
    accuracy: float
    avg_latency: float
    total_tokens: int
    branch: str = "main"
