from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ConnectionType(str, Enum):
    SERVICE_NAME = "service_name"
    SID = "sid"


class ConnectionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class ConnectionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    host: str = Field(..., min_length=1, max_length=255)
    port: int = Field(default=1521, ge=1, le=65535)
    service_name: Optional[str] = None
    sid: Optional[str] = None
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1)
    connection_type: ConnectionType = ConnectionType.SERVICE_NAME


class ConnectionUpdate(BaseModel):
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    service_name: Optional[str] = None
    sid: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class ConnectionResponse(BaseModel):
    id: str
    name: str
    host: str
    port: int
    service_name: Optional[str] = None
    sid: Optional[str] = None
    connection_type: ConnectionType
    status: ConnectionStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ConnectionTestResult(BaseModel):
    success: bool
    message: str
    server_version: Optional[str] = None


class TableInfo(BaseModel):
    schema_name: str
    table_name: str
    table_type: str
    row_count: Optional[int] = None
    columns: List["ColumnInfo"] = []
    primary_key: Optional["PrimaryKeyInfo"] = None
    foreign_keys: List["ForeignKeyInfo"] = []
    indexes: List["IndexInfo"] = []


class ColumnInfo(BaseModel):
    name: str
    data_type: str
    nullable: bool
    default_value: Optional[str] = None
    character_max_length: Optional[int] = None
    numeric_precision: Optional[int] = None
    numeric_scale: Optional[int] = None


class PrimaryKeyInfo(BaseModel):
    name: str
    columns: List[str]


class ForeignKeyInfo(BaseModel):
    name: str
    columns: List[str]
    referenced_schema: str
    referenced_table: str
    referenced_columns: List[str]
    delete_rule: Optional[str] = None


class IndexInfo(BaseModel):
    name: str
    columns: List[str]
    index_type: str
    uniqueness: str
    status: Optional[str] = None


class ERDData(BaseModel):
    tables: List[TableInfo]
    relationships: List[Dict[str, Any]]


class DataGroupCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    color: str = Field(default="#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$")
    parent_id: Optional[str] = None
    connection_id: Optional[str] = None


class DataGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    parent_id: Optional[str] = None


class DataGroupResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    color: str
    parent_id: Optional[str] = None
    connection_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    tables: List["GroupTableResponse"] = []
    
    class Config:
        from_attributes = True


class GroupTableResponse(BaseModel):
    id: str
    schema_name: str
    table_name: str
    
    class Config:
        from_attributes = True


class AIQueryRequest(BaseModel):
    connection_id: str
    natural_language: str = Field(..., min_length=1)
    context_schema: Optional[str] = None
    max_rows: int = Field(default=100, ge=1, le=10000)


class AIQueryResponse(BaseModel):
    query_id: str
    generated_sql: str
    explanation: Optional[str] = None
    tables_used: List[str] = []
    execution_time_ms: Optional[int] = None
    row_count: Optional[int] = None
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


class VectorCollectionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    connection_id: str
    source_schema: str
    source_table: str
    embedding_model: str = Field(default="text-embedding-3-small")
    text_columns: List[str] = []
    batch_size: int = Field(default=100, ge=1, le=1000)


class VectorCollectionResponse(BaseModel):
    id: str
    name: str
    connection_id: str
    source_schema: str
    source_table: str
    embedding_model: str
    vector_dimension: int
    status: str
    record_count: int
    last_sync_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class VectorSearchRequest(BaseModel):
    collection_id: str
    query: str
    top_k: int = Field(default=5, ge=1, le=100)
    filter: Optional[Dict[str, Any]] = None


class VectorSearchResponse(BaseModel):
    results: List["VectorSearchResult"]
    query_time_ms: int


class VectorSearchResult(BaseModel):
    id: str
    score: float
    document: Dict[str, Any]
    metadata: Dict[str, Any]


class SyncStatusResponse(BaseModel):
    collection_id: str
    status: str
    progress: float
    records_processed: int
    total_records: int
    error: Optional[str] = None


TableInfo.model_rebuild()
DataGroupResponse.model_rebuild()
VectorSearchResponse.model_rebuild()
