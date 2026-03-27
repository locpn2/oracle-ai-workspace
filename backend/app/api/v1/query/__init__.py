from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse
import time
import csv
import json
import io
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
async def preview_sql(sql: str = Body(..., embed=True)):
    try:
        result = await oracle_db.execute_query(f"EXPLAIN PLAN FOR {sql}", 1, 10)
        return {
            "valid": True,
            "plan": result.get("rows", []),
            "message": "Query is valid for execution"
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}


@router.post("/explain")
async def explain_query(request: dict):
    """Get query execution plan"""
    sql = request.get("sql", "")
    try:
        explain_sql = f"EXPLAIN PLAN FOR {sql}"
        result = await oracle_db.execute_query(explain_sql, 1, 100)
        
        plan_output = []
        for row in result.get("rows", []):
            plan_output.append({
                "operation": row.get("OPERATION", ""),
                "object_name": row.get("OBJECT_NAME", ""),
                "options": row.get("OPTIONS", ""),
            })
        
        return {
            "sql": sql,
            "plan": plan_output,
            "estimated_rows": result.get("total_rows", 0)
        }
    except Exception as e:
        return {
            "sql": sql,
            "plan": [],
            "error": str(e),
            "estimated_rows": 0
        }


@router.post("/export")
async def export_results(request: ExecuteRequest):
    """Export query results in various formats"""
    try:
        result = await oracle_db.execute_query(request.sql, 1, 10000)
        
        if request.format == "json":
            return {
                "columns": result["columns"],
                "rows": result["rows"],
                "total_rows": result["total_rows"]
            }
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=result["columns"])
        writer.writeheader()
        for row in result["rows"]:
            writer.writerow(row)
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=query_results.csv"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
