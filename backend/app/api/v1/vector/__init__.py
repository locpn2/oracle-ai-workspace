from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from ....services.vector import vector_service, sync_status
from ....llm.ollama import ollama_client

router = APIRouter()


class SyncRequest(BaseModel):
    table_name: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    table_name: str
    column_name: Optional[str]
    description: str
    similarity: float


@router.post("/sync")
async def trigger_sync(request: SyncRequest = None):
    """Trigger schema sync to vector database"""
    try:
        if request and request.table_name:
            success = await vector_service.sync_table(request.table_name)
            if success:
                return {
                    "message": f"Table {request.table_name} synced successfully",
                    "table_name": request.table_name
                }
            else:
                raise HTTPException(status_code=500, detail=f"Failed to sync table {request.table_name}")
        
        result = await vector_service.sync_full_schema()
        if result.get("success"):
            return {
                "message": "Full schema sync completed",
                "tables_synced": result.get("tables_synced"),
                "total_tables": result.get("total_tables"),
                "last_sync": result.get("last_sync")
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Sync failed"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_sync_status():
    """Get current vector sync status"""
    try:
        status = vector_service.get_sync_status()
        embedding_count = vector_service.vector_db.get_embedding_count()
        tables_count = vector_service.vector_db.get_tables_count()
        
        return {
            **status,
            "embedding_count": embedding_count,
            "unique_tables": tables_count
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "last_sync": None,
            "tables_synced": 0,
            "total_tables": 0,
            "embedding_count": 0,
            "unique_tables": 0
        }


@router.post("/search")
async def semantic_search(request: SearchRequest):
    """Search schema using semantic similarity"""
    try:
        results = await vector_service.semantic_search(request.query, request.top_k)
        return {
            "query": request.query,
            "results": [
                {
                    "table_name": r.get("table_name"),
                    "column_name": r.get("column_name"),
                    "description": r.get("description"),
                    "similarity": round(r.get("similarity", 0), 4)
                }
                for r in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear")
async def clear_embeddings():
    """Clear all vector embeddings"""
    try:
        success = vector_service.clear_all_embeddings()
        if success:
            return {"message": "All embeddings cleared successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear embeddings")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models():
    """List available Ollama models"""
    try:
        models = await ollama_client.list_models()
        available = await ollama_client.is_available()
        return {
            "available": available,
            "models": models,
            "current_model": ollama_client.model,
            "current_embed_model": ollama_client.embed_model
        }
    except Exception as e:
        return {
            "available": False,
            "models": [],
            "error": str(e)
        }
