from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import get_db
from app.models.orm import Connection
from app.models.schemas import TableInfo, ColumnInfo, PrimaryKeyInfo, ForeignKeyInfo, IndexInfo, ERDData
from app.services.oracle_client import OracleClient
from app.api.v1.connections import decrypt_password

router = APIRouter(prefix="/schemas", tags=["schemas"])


def get_oracle_client(connection_id: str, db: Session) -> OracleClient:
    conn = db.query(Connection).filter(Connection.id == connection_id).first()
    if not conn:
        raise HTTPException(status_code=404, detail="Connection not found")
    
    from app.services.oracle_client import OracleConnectionConfig
    config = OracleConnectionConfig(
        host=conn.host,
        port=conn.port,
        username=conn.username,
        password=decrypt_password(conn.password_encrypted),
        service_name=conn.service_name,
        sid=conn.sid,
        connection_type=conn.connection_type
    )
    return OracleClient(config)


@router.get("/{connection_id}/schemas", response_model=List[str])
def list_schemas(connection_id: str, db: Session = Depends(get_db)):
    client = get_oracle_client(connection_id, db)
    try:
        return client.get_schemas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{connection_id}/schemas/{schema_name}/tables", response_model=List[dict])
def list_tables(connection_id: str, schema_name: str, db: Session = Depends(get_db)):
    client = get_oracle_client(connection_id, db)
    try:
        return client.get_tables(schema_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{connection_id}/schemas/{schema_name}/tables/{table_name}", response_model=TableInfo)
def get_table_details(
    connection_id: str,
    schema_name: str,
    table_name: str,
    db: Session = Depends(get_db)
):
    client = get_oracle_client(connection_id, db)
    try:
        columns = client.get_columns(schema_name, table_name)
        primary_keys = client.get_primary_keys(schema_name, table_name)
        foreign_keys = client.get_foreign_keys(schema_name, table_name)
        indexes = client.get_indexes(schema_name, table_name)
        
        column_infos = [
            ColumnInfo(
                name=c["name"],
                data_type=c["data_type"],
                nullable=c["nullable"],
                default_value=c.get("default_value"),
                character_max_length=c.get("character_max_length"),
                numeric_precision=c.get("numeric_precision"),
                numeric_scale=c.get("numeric_scale")
            )
            for c in columns
        ]
        
        pk_info = None
        if primary_keys:
            pk_info = PrimaryKeyInfo(name=f"PK_{table_name}", columns=primary_keys)
        
        fk_infos = [
            ForeignKeyInfo(
                name=fk["name"],
                columns=fk["columns"],
                referenced_schema=fk["referenced_schema"],
                referenced_table=fk["referenced_table"],
                referenced_columns=fk["referenced_columns"],
                delete_rule=fk.get("delete_rule")
            )
            for fk in foreign_keys
        ]
        
        idx_infos = [
            IndexInfo(
                name=idx["name"],
                columns=idx["columns"],
                index_type=idx["index_type"],
                uniqueness=idx["uniqueness"],
                status=idx.get("status")
            )
            for idx in indexes
        ]
        
        return TableInfo(
            schema_name=schema_name,
            table_name=table_name,
            table_type="TABLE",
            columns=column_infos,
            primary_key=pk_info,
            foreign_keys=fk_infos,
            indexes=idx_infos
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{connection_id}/erd", response_model=ERDData)
def get_erd_data(
    connection_id: str,
    schema_name: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    client = get_oracle_client(connection_id, db)
    try:
        schemas = [schema_name] if schema_name else client.get_schemas()
        
        all_tables = []
        all_relationships = []
        
        for schema in schemas:
            tables = client.get_tables(schema)
            
            for table in tables:
                table_name = table["name"]
                columns = client.get_columns(schema, table_name)
                primary_keys = client.get_primary_keys(schema, table_name)
                foreign_keys = client.get_foreign_keys(schema, table_name)
                
                column_infos = [
                    ColumnInfo(
                        name=c["name"],
                        data_type=c["data_type"],
                        nullable=c["nullable"],
                        default_value=c.get("default_value"),
                        character_max_length=c.get("character_max_length"),
                        numeric_precision=c.get("numeric_precision"),
                        numeric_scale=c.get("numeric_scale")
                    )
                    for c in columns
                ]
                
                pk_info = None
                if primary_keys:
                    pk_info = PrimaryKeyInfo(name=f"PK_{table_name}", columns=primary_keys)
                
                table_info = TableInfo(
                    schema_name=schema,
                    table_name=table_name,
                    table_type="TABLE",
                    row_count=table.get("row_count"),
                    columns=column_infos,
                    primary_key=pk_info,
                    foreign_keys=[],
                    indexes=[]
                )
                all_tables.append(table_info)
                
                for fk in foreign_keys:
                    relationship = {
                        "from_schema": schema,
                        "from_table": table_name,
                        "from_columns": fk["columns"],
                        "to_schema": fk["referenced_schema"],
                        "to_table": fk["referenced_table"],
                        "to_columns": fk["referenced_columns"],
                        "constraint_name": fk["name"],
                        "delete_rule": fk.get("delete_rule")
                    }
                    all_relationships.append(relationship)
        
        return ERDData(tables=all_tables, relationships=all_relationships)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{connection_id}/query")
def execute_query(
    connection_id: str,
    sql: str = Query(...),
    fetch_size: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    client = get_oracle_client(connection_id, db)
    try:
        success, columns, rows, error = client.execute_query(sql, fetch_size=fetch_size)
        
        if not success:
            raise HTTPException(status_code=400, detail=error)
        
        return {
            "success": True,
            "columns": columns,
            "rows": [list(row) for row in rows],
            "row_count": len(rows),
            "truncated": len(rows) == fetch_size
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
