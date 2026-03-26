from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
import time
from app.models.database import get_db
from app.models.orm import Connection, QueryHistory
from app.models.schemas import AIQueryRequest, AIQueryResponse
from app.services.ai_service import AIService
from app.services.oracle_client import OracleClient
from app.api.v1.connections import decrypt_password

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/query", response_model=AIQueryResponse)
def text_to_sql_query(request: AIQueryRequest, db: Session = Depends(get_db)):
    conn = db.query(Connection).filter(Connection.id == request.connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    oracle_config = OracleClient(
        OracleConnectionConfig(
            host=conn.host,
            port=conn.port,
            username=conn.username,
            password=decrypt_password(conn.password_encrypted),
            service_name=conn.service_name,
            sid=conn.sid,
            connection_type=conn.connection_type
        )
    )
    
    ai_service = AIService()
    
    schema_context = {"tables": []}
    try:
        schemas = oracle_config.get_schemas()
        target_schema = request.context_schema or (schemas[0] if schemas else None)
        
        if target_schema:
            tables = oracle_config.get_tables(target_schema)
            for table in tables[:20]:
                columns = oracle_config.get_columns(target_schema, table["name"])
                pks = oracle_config.get_primary_keys(target_schema, table["name"])
                fks = oracle_config.get_foreign_keys(target_schema, table["name"])
                
                schema_context["tables"].append({
                    "name": f"{target_schema}.{table['name']}",
                    "columns": columns,
                    "primary_keys": pks,
                    "foreign_keys": fks
                })
    except Exception:
        pass
    
    query_id = str(uuid.uuid4())
    generated_sql, explanation, tables_used = ai_service.generate_sql(
        natural_language=request.natural_language,
        schema_context=schema_context,
        connection_id=request.connection_id
    )
    
    history = QueryHistory(
        id=query_id,
        connection_id=request.connection_id,
        natural_language=request.natural_language,
        generated_sql=generated_sql,
        success="1" if generated_sql else "0"
    )
    db.add(history)
    db.commit()
    
    return AIQueryResponse(
        query_id=query_id,
        generated_sql=generated_sql,
        explanation=explanation,
        tables_used=tables_used
    )


@router.post("/query/execute")
def execute_generated_query(
    connection_id: str,
    sql: str,
    max_rows: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    conn = db.query(Connection).filter(Connection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    oracle_config = OracleClient(
        OracleConnectionConfig(
            host=conn.host,
            port=conn.port,
            username=conn.username,
            password=decrypt_password(conn.password_encrypted),
            service_name=conn.service_name,
            sid=conn.sid,
            connection_type=conn.connection_type
        )
    )
    
    start_time = time.time()
    success, columns, rows, error = oracle_config.execute_query(sql, fetch_size=max_rows)
    execution_time = int((time.time() - start_time) * 1000)
    
    if not success:
        raise HTTPException(status_code=400, detail=error)
    
    return {
        "success": True,
        "columns": columns,
        "rows": [list(row) for row in rows],
        "row_count": len(rows),
        "execution_time_ms": execution_time,
        "truncated": len(rows) == max_rows
    }


@router.get("/query/history", response_model=List[dict])
def get_query_history(
    connection_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(QueryHistory)
    if connection_id:
        query = query.filter(QueryHistory.connection_id == connection_id)
    
    history = query.order_by(QueryHistory.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": h.id,
            "connection_id": h.connection_id,
            "natural_language": h.natural_language,
            "generated_sql": h.generated_sql,
            "execution_time_ms": h.execution_time_ms,
            "row_count": h.row_count,
            "success": h.success == "1",
            "error_message": h.error_message,
            "created_at": h.created_at
        }
        for h in history
    ]


@router.post("/query/explain")
def explain_query(
    connection_id: str,
    sql: str,
    db: Session = Depends(get_db)
):
    ai_service = AIService()
    
    explanation = ai_service.explain_query(sql, {})
    
    return {
        "sql": sql,
        "explanation": explanation
    }
