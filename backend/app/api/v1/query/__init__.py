from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse
import time
import asyncio
import csv
import json
import io
from ....models.query import QueryRequest, QueryResponse, ExecuteRequest, ExecuteResponse, QueryHistory
from ....db.oracle import oracle_db
from ....db.postgres import query_history_db
from ....services.text_to_sql import text_to_sql_service
from ....core.config import get_settings

settings = get_settings()
router = APIRouter()

QUERY_HISTORY = []

@router.post("/text-to-sql", response_model=QueryResponse)
async def text_to_sql(request: QueryRequest):
    start_time = time.time()
    try:
        timeout = settings.llm_request_timeout
        result = await asyncio.wait_for(
            text_to_sql_service.convert(request.natural_language, request.context),
            timeout=timeout
        )

        has_sql = bool(result.get("sql"))
        has_error = bool(result.get("error"))
        success = has_sql and not has_error
        elapsed_ms = int((time.time() - start_time) * 1000)

        query_data = {
            "id": str(len(QUERY_HISTORY) + 1),
            "natural_language": request.natural_language,
            "sql": result.get("sql", ""),
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "success": success,
        }
        QUERY_HISTORY.insert(0, query_data)

        try:
            query_history_db.add_query(
                user_id=None,
                natural_language=request.natural_language,
                generated_sql=result.get("sql", ""),
                success=success,
                execution_time_ms=elapsed_ms,
            )
        except Exception as db_err:
            print(f"Failed to persist query history: {db_err}")

        return QueryResponse(**result)
    except asyncio.TimeoutError:
        elapsed_ms = int((time.time() - start_time) * 1000)
        try:
            query_history_db.add_query(
                user_id=None,
                natural_language=request.natural_language,
                generated_sql="",
                success=False,
                execution_time_ms=elapsed_ms,
            )
        except Exception:
            pass
        raise HTTPException(
            status_code=504,
            detail=f"Request timed out after {settings.llm_request_timeout}s."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/text-to-sql/stream")
async def text_to_sql_stream(request: QueryRequest):
    """Stream text-to-SQL conversion progress via Server-Sent Events"""
    async def event_generator():
        try:
            yield f"data: {json.dumps({'status': 'processing', 'message': 'Analyzing query...'})}\n\n"

            ollama_ready = await text_to_sql_service.is_ollama_available()
            if not ollama_ready:
                yield f"data: {json.dumps({'status': 'fallback', 'message': 'LLM unavailable, using template fallback'})}\n\n"
            else:
                yield f"data: {json.dumps({'status': 'generating', 'message': 'Generating SQL via LLM...'})}\n\n"

            result = await text_to_sql_service.convert(
                request.natural_language, request.context
            )

            yield f"data: {json.dumps({'status': 'complete', 'result': result})}\n\n"

            # Persist history
            has_sql = bool(result.get("sql"))
            has_error = bool(result.get("error"))
            try:
                query_history_db.add_query(
                    user_id=None,
                    natural_language=request.natural_language,
                    generated_sql=result.get("sql", ""),
                    success=has_sql and not has_error,
                    execution_time_ms=0,
                )
            except Exception:
                pass

        except Exception as e:
            yield f"data: {json.dumps({'status': 'error', 'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
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
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=list[QueryHistory])
async def get_history(limit: int = 50, use_db: bool = False):
    if use_db:
        try:
            rows = query_history_db.get_history(limit=limit)
            return [
                QueryHistory(
                    id=str(r["id"]),
                    natural_language=r["natural_language"],
                    sql=r["generated_sql"],
                    created_at=str(r["created_at"]),
                    success=r["success"],
                )
                for r in rows
            ]
        except Exception as db_err:
            print(f"DB history query failed, falling back to in-memory: {db_err}")
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

        if request.format == "xlsx":
            from openpyxl import Workbook
            wb = Workbook()
            ws = wb.active
            ws.append(result["columns"])
            for row in result["rows"]:
                ws.append([row.get(col, "") for col in result["columns"]])

            output = io.BytesIO()
            wb.save(output)
            output.seek(0)

            return StreamingResponse(
                output,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=query_results.xlsx"}
            )

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
