from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.orm import Connection, ConnectionStatus
from app.models.schemas import (
    ConnectionCreate, ConnectionUpdate, ConnectionResponse,
    ConnectionTestResult, ConnectionType
)
from app.services.oracle_client import OracleClient, OracleConnectionConfig
from cryptography.fernet import Fernet
import base64
import hashlib

router = APIRouter(prefix="/connections", tags=["connections"])

ENCRYPTION_KEY = Fernet.generate_key()
fernet = Fernet(ENCRYPTION_KEY)


def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()


@router.post("", response_model=ConnectionResponse, status_code=status.HTTP_201_CREATED)
def create_connection(conn: ConnectionCreate, db: Session = Depends(get_db)):
    password_encrypted = encrypt_password(conn.password)
    
    db_conn = Connection(
        name=conn.name,
        host=conn.host,
        port=conn.port,
        service_name=conn.service_name,
        sid=conn.sid,
        username=conn.username,
        password_encrypted=password_encrypted,
        connection_type=conn.connection_type.value,
        status=ConnectionStatus.INACTIVE
    )
    
    db.add(db_conn)
    db.commit()
    db.refresh(db_conn)
    
    return db_conn


@router.get("", response_model=List[ConnectionResponse])
def list_connections(db: Session = Depends(get_db)):
    connections = db.query(Connection).all()
    return connections


@router.get("/{connection_id}", response_model=ConnectionResponse)
def get_connection(connection_id: str, db: Session = Depends(get_db)):
    conn = db.query(Connection).filter(Connection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")
    return conn


@router.put("/{connection_id}", response_model=ConnectionResponse)
def update_connection(
    connection_id: str,
    conn_update: ConnectionUpdate,
    db: Session = Depends(get_db)
):
    conn = db.query(Connection).filter(Connection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    update_data = conn_update.model_dump(exclude_unset=True)
    
    if "password" in update_data:
        update_data["password_encrypted"] = encrypt_password(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(conn, key, value)
    
    db.commit()
    db.refresh(conn)
    return conn


@router.delete("/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connection(connection_id: str, db: Session = Depends(get_db)):
    conn = db.query(Connection).filter(Connection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    db.delete(conn)
    db.commit()


@router.post("/{connection_id}/test", response_model=ConnectionTestResult)
def test_connection(connection_id: str, db: Session = Depends(get_db)):
    conn = db.query(Connection).filter(Connection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    config = OracleConnectionConfig(
        host=conn.host,
        port=conn.port,
        username=conn.username,
        password=decrypt_password(conn.password_encrypted),
        service_name=conn.service_name,
        sid=conn.sid,
        connection_type=conn.connection_type
    )
    
    client = OracleClient(config)
    success, message, version = client.test_connection()
    
    if success:
        conn.status = ConnectionStatus.ACTIVE
    else:
        conn.status = ConnectionStatus.ERROR
    db.commit()
    
    return ConnectionTestResult(
        success=success,
        message=message,
        server_version=version
    )


@router.post("/test-direct", response_model=ConnectionTestResult)
def test_connection_direct(conn: ConnectionCreate):
    config = OracleConnectionConfig(
        host=conn.host,
        port=conn.port,
        username=conn.username,
        password=conn.password,
        service_name=conn.service_name,
        sid=conn.sid,
        connection_type=conn.connection_type.value
    )
    
    client = OracleClient(config)
    success, message, version = client.test_connection()
    
    return ConnectionTestResult(
        success=success,
        message=message,
        server_version=version
    )
