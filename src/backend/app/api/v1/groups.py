from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.orm import DataGroup, GroupTable, Connection
from app.models.schemas import (
    DataGroupCreate, DataGroupUpdate, DataGroupResponse, GroupTableResponse
)

router = APIRouter(prefix="/groups", tags=["groups"])


@router.post("", response_model=DataGroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(group: DataGroupCreate, db: Session = Depends(get_db)):
    if group.connection_id:
        conn = db.query(Connection).filter(Connection.id == group.connection_id).first()
        if not conn:
            raise HTTPException(status_code=404, detail="Connection not found")
    
    db_group = DataGroup(
        name=group.name,
        description=group.description,
        color=group.color,
        parent_id=group.parent_id,
        connection_id=group.connection_id
    )
    
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    return db_group


@router.get("", response_model=List[DataGroupResponse])
def list_groups(
    connection_id: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(DataGroup)
    if connection_id:
        query = query.filter(DataGroup.connection_id == connection_id)
    
    groups = query.all()
    return groups


@router.get("/{group_id}", response_model=DataGroupResponse)
def get_group(group_id: str, db: Session = Depends(get_db)):
    group = db.query(DataGroup).filter(DataGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group


@router.put("/{group_id}", response_model=DataGroupResponse)
def update_group(
    group_id: str,
    group_update: DataGroupUpdate,
    db: Session = Depends(get_db)
):
    group = db.query(DataGroup).filter(DataGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    update_data = group_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(group, key, value)
    
    db.commit()
    db.refresh(group)
    return group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: str, db: Session = Depends(get_db)):
    group = db.query(DataGroup).filter(DataGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db.delete(group)
    db.commit()


@router.post("/{group_id}/tables", response_model=GroupTableResponse)
def add_tables_to_group(
    group_id: str,
    connection_id: str,
    schema_name: str,
    table_name: str,
    db: Session = Depends(get_db)
):
    group = db.query(DataGroup).filter(DataGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    existing = db.query(GroupTable).filter(
        GroupTable.group_id == group_id,
        GroupTable.connection_id == connection_id,
        GroupTable.schema_name == schema_name,
        GroupTable.table_name == table_name
    ).first()
    
    if existing:
        return existing
    
    group_table = GroupTable(
        group_id=group_id,
        connection_id=connection_id,
        schema_name=schema_name,
        table_name=table_name
    )
    
    db.add(group_table)
    db.commit()
    db.refresh(group_table)
    
    return group_table


@router.delete("/{group_id}/tables/{table_id}")
def remove_table_from_group(
    group_id: str,
    table_id: str,
    db: Session = Depends(get_db)
):
    group_table = db.query(GroupTable).filter(
        GroupTable.id == table_id,
        GroupTable.group_id == group_id
    ).first()
    
    if not group_table:
        raise HTTPException(status_code=404, detail="Table not found in group")
    
    db.delete(group_table)
    db.commit()
    
    return {"message": "Table removed from group"}


@router.get("/{group_id}/tables", response_model=List[GroupTableResponse])
def get_group_tables(group_id: str, db: Session = Depends(get_db)):
    group = db.query(DataGroup).filter(DataGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    tables = db.query(GroupTable).filter(GroupTable.group_id == group_id).all()
    return tables
