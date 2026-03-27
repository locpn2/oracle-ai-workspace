from fastapi import APIRouter, HTTPException
from ....models.query import QueryResponse

router = APIRouter()

SYNC_STATUS = {
    "last_sync": None,
    "status": "idle",
    "tables_synced": 0,
}


@router.post("/sync")
async def sync_to_vector():
    SYNC_STATUS["status"] = "syncing"
    SYNC_STATUS["last_sync"] = "2024-01-01T00:00:00"
    SYNC_STATUS["tables_synced"] = 42
    SYNC_STATUS["status"] = "completed"
    return {"message": "Sync completed", "status": SYNC_STATUS}


@router.get("/status")
async def get_sync_status():
    return SYNC_STATUS


@router.post("/search")
async def semantic_search(query: str, top_k: int = 5):
    return {
        "query": query,
        "results": [
            {"table": "CUSTOMERS", "score": 0.95, "reason": "Customer data matches query"},
            {"table": "ORDERS", "score": 0.87, "reason": "Order information relevant"},
        ][:top_k]
    }
