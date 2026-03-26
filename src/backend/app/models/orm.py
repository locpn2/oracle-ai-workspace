import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
import enum
from app.models.database import Base


class ConnectionStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class SyncStatus(str, enum.Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Connection(Base):
    __tablename__ = "connections"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    host = Column(String(255), nullable=False)
    port = Column(Integer, default=1521)
    service_name = Column(String(100), nullable=True)
    sid = Column(String(100), nullable=True)
    username = Column(String(100), nullable=False)
    password_encrypted = Column(Text, nullable=False)
    connection_type = Column(String(20), default="service_name")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(SQLEnum(ConnectionStatus), default=ConnectionStatus.INACTIVE)
    
    groups = relationship("DataGroup", back_populates="connection")
    vector_collections = relationship("VectorCollection", back_populates="connection")


class DataGroup(Base):
    __tablename__ = "data_groups"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(7), default="#3B82F6")
    parent_id = Column(String(36), ForeignKey("data_groups.id"), nullable=True)
    connection_id = Column(String(36), ForeignKey("connections.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    connection = relationship("Connection", back_populates="groups")
    parent = relationship("DataGroup", remote_side=[id], backref="children")
    tables = relationship("GroupTable", back_populates="group", cascade="all, delete-orphan")


class GroupTable(Base):
    __tablename__ = "group_tables"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    group_id = Column(String(36), ForeignKey("data_groups.id", ondelete="CASCADE"), nullable=False)
    connection_id = Column(String(36), ForeignKey("connections.id", ondelete="CASCADE"), nullable=False)
    schema_name = Column(String(100), nullable=False)
    table_name = Column(String(100), nullable=False)
    
    group = relationship("DataGroup", back_populates="tables")


class VectorCollection(Base):
    __tablename__ = "vector_collections"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    connection_id = Column(String(36), ForeignKey("connections.id", ondelete="CASCADE"), nullable=False)
    source_schema = Column(String(100), nullable=False)
    source_table = Column(String(100), nullable=False)
    embedding_model = Column(String(100), default="text-embedding-3-small")
    text_columns = Column(Text, nullable=True)
    vector_dimension = Column(Integer, default=1536)
    status = Column(SQLEnum(SyncStatus), default=SyncStatus.IDLE)
    last_sync_at = Column(DateTime, nullable=True)
    record_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    connection = relationship("Connection", back_populates="vector_collections")


class QueryHistory(Base):
    __tablename__ = "query_history"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    connection_id = Column(String(36), ForeignKey("connections.id", ondelete="CASCADE"), nullable=False)
    natural_language = Column(Text, nullable=False)
    generated_sql = Column(Text, nullable=False)
    execution_time_ms = Column(Integer, nullable=True)
    row_count = Column(Integer, nullable=True)
    success = Column(String(1), default="1")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
