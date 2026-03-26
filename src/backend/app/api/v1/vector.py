from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
from app.models.database import get_db
from app.models.orm import VectorCollection, Connection, SyncStatus
from app.models.schemas import (
    VectorCollectionCreate, VectorCollectionResponse,
    VectorSearchRequest, VectorSearchResponse, VectorSearchResult,
    SyncStatusResponse
)
from app.services.vector_service import VectorService
from app.services.oracle_client import OracleClient
from app.api.v1.connections import decrypt_password

router = APIRouter(prefix="/vector", tags=["vector"])


@router.get("/collections", response_model=List[VectorCollectionResponse])
def list_vector_collections(db: Session = Depends(get_db)):
    collections = db.query(VectorCollection).all()
    return collections


@router.post("/collections", response_model=VectorCollectionResponse)
def create_vector_collection(
    collection: VectorCollectionCreate,
    db: Session = Depends(get_db)
):
    conn = db.query(Connection).filter(Connection.id == collection.connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    existing = db.query(VectorCollection).filter(
        VectorCollection.connection_id == collection.connection_id,
        VectorCollection.source_schema == collection.source_schema,
        VectorCollection.source_table == collection.source_table
    ).first()
    
    if existing:
        return existing
    
    db_collection = VectorCollection(
        name=collection.name,
        connection_id=collection.connection_id,
        source_schema=collection.source_schema,
        source_table=collection.source_table,
        embedding_model=collection.embedding_model,
        text_columns=",".join(collection.text_columns) if collection.text_columns else None,
        status=SyncStatus.IDLE
    )
    
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    
    return db_collection


@router.delete("/collections/{collection_id}")
def delete_vector_collection(collection_id: str, db: Session = Depends(get_db)):
    collection = db.query(VectorCollection).filter(VectorCollection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    vector_service = VectorService()
    vector_service.delete_collection(collection.name)
    
    db.delete(collection)
    db.commit()
    
    return {"message": "Collection deleted"}


@router.post("/sync/{collection_id}")
def trigger_sync(
    collection_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    collection = db.query(VectorCollection).filter(VectorCollection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    collection.status = SyncStatus.RUNNING
    db.commit()
    
    background_tasks.add_task(
        sync_collection_task,
        collection_id=collection_id,
        db_url=str(db.bind.url)
    )
    
    return {"message": "Sync started", "collection_id": collection_id}


def sync_collection_task(collection_id: str, db_url: str):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        collection = db.query(VectorCollection).filter(VectorCollection.id == collection_id).first()
        if not collection:
            return
        
        conn = db.query(Connection).filter(Connection.id == collection.connection_id).first()
        
        oracle_client = OracleClient(
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
        
        columns, rows = oracle_client.get_table_data(
            collection.source_schema,
            collection.source_table,
            limit=10000
        )
        
        text_columns = collection.text_columns.split(",") if collection.text_columns else None
        
        vector_service = VectorService()
        collection_name = f"{collection.source_schema}_{collection.source_table}"
        
        table_data = []
        for row in rows:
            row_dict = {columns[i]: row[i] for i in range(len(columns))}
            table_data.append(row_dict)
        
        embedded, failed = vector_service.vectorize_table(
            collection_name=collection_name,
            table_data=table_data,
            columns=columns,
            text_columns=text_columns or columns,
            batch_size=100
        )
        
        collection.status = SyncStatus.COMPLETED
        collection.last_sync_at = datetime.utcnow()
        collection.record_count = embedded
        
        if collection.name != collection_name:
            collection_name = collection.name
        
        vector_service.create_collection(collection_name)
        
        db.commit()
        
    except Exception as e:
        collection.status = SyncStatus.FAILED
        db.commit()
    finally:
        db.close()


@router.get("/sync/status/{collection_id}", response_model=SyncStatusResponse)
def get_sync_status(collection_id: str, db: Session = Depends(get_db)):
    collection = db.query(VectorCollection).filter(VectorCollection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    progress = 0.0
    if collection.status == SyncStatus.COMPLETED:
        progress = 100.0
    elif collection.status == SyncStatus.RUNNING:
        progress = 50.0
    
    return SyncStatusResponse(
        collection_id=collection_id,
        status=collection.status.value,
        progress=progress,
        records_processed=collection.record_count or 0,
        total_records=collection.record_count or 0
    )


@router.post("/search", response_model=VectorSearchResponse)
def semantic_search(request: VectorSearchRequest, db: Session = Depends(get_db)):
    collection = db.query(VectorCollection).filter(VectorCollection.id == request.collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    vector_service = VectorService()
    import time
    start_time = time.time()
    
    results = vector_service.search(
        collection_name=collection.name,
        query=request.query,
        top_k=request.top_k,
        filter_metadata=request.filter
    )
    
    query_time = int((time.time() - start_time) * 1000)
    
    search_results = [
        VectorSearchResult(
            id=r["id"],
            score=r["score"],
            document={"text": r["document"]},
            metadata=r["metadata"]
        )
        for r in results
    ]
    
    return VectorSearchResponse(
        results=search_results,
        query_time_ms=query_time
    )


@router.get("/stats/{collection_id}")
def get_collection_stats(collection_id: str, db: Session = Depends(get_db)):
    collection = db.query(VectorCollection).filter(VectorCollection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    vector_service = VectorService()
    stats = vector_service.get_collection_stats(collection.name)
    
    return {
        "collection_id": collection_id,
        "name": collection.name,
        "status": collection.status.value,
        "source": f"{collection.source_schema}.{collection.source_table}",
        "record_count": collection.record_count,
        "last_sync": collection.last_sync_at,
        "vector_stats": stats
    }
