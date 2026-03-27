from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    natural_language: str
    context: Optional[str] = None


class QueryResponse(BaseModel):
    sql: str
    confidence: float
    explanation: Optional[str] = None
    error: Optional[str] = None


class ExecuteRequest(BaseModel):
    sql: str
    page: int = 1
    page_size: int = 100
    format: str = "csv"


class ExecuteResponse(BaseModel):
    columns: list[str]
    rows: list[dict]
    total_rows: int
    page: int
    page_size: int
    execution_time: float
    error: Optional[str] = None


class QueryHistory(BaseModel):
    id: str
    natural_language: str
    sql: str
    created_at: str
    success: bool
