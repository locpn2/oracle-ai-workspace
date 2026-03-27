from fastapi import APIRouter, HTTPException
import time
from ....models.query import QueryRequest, QueryResponse, ExecuteRequest, ExecuteResponse, QueryHistory
from ....db.oracle import oracle_db
from ....services.text_to_sql import text_to_sql_service

router = APIRouter()

QUERY_HISTORY = []


@router.post("/text-to-sql", response_model=QueryResponse)
async def text_to_sql(request: QueryRequest):
    try:
        result = await text_to_sql_service.convert(request.natural_language, request.context)
        
        QUERY_HISTORY.insert(0, {
            "id": str(len(QUERY_HISTORY) + 1),
            "natural_language": request.natural_language,
            "sql": result["sql"],
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "success": not result.get("error"),
        })
        
        return QueryResponse(**result)
    except Exception as e:
        return QueryResponse(
            sql="",
            confidence=0,
            error=str(e),
        )


@router.post("/execute", response_model=ExecuteResponse)
async def execute_query(request: ExecuteRequest):
    try:
        start_time = time.time()
        result = await oracle_db.execute_query(request.sql, request.page, request.page_size)
        execution_time = (time.time() - start_time) * 1000
        
        return ExecuteResponse(
            columns=result["columns"],
            rows=result["rows"],
            total_rows=result["total_rows"],
            page=result["page"],
            page_size=result["page_size"],
            execution_time=round(execution_time, 2),
        )
    except Exception as e:
        return ExecuteResponse(
            columns=[],
            rows=[],
            total_rows=0,
            page=1,
            page_size=100,
            execution_time=0,
            error=str(e),
        )


@router.get("/history", response_model=list[QueryHistory])
async def get_history(limit: int = 50):
    return QUERY_HISTORY[:limit]


@router.post("/preview")
async def preview_sql(sql: str):
    try:
        await oracle_db.execute_query(f"EXPLAIN PLAN FOR {sql}")
        return {"valid": True}
    except Exception as e:
        return {"valid": False, "error": str(e)}
