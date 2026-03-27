from fastapi import APIRouter, Depends, HTTPException
from ....models.schema import Table, ERDData, ERDNode, ERDEdge, SchemaGroup, SchemaGroupCreate
from ....db.oracle import oracle_db

router = APIRouter()

GROUPS = []


@router.get("/tables", response_model=list[Table])
async def get_tables():
    try:
        tables_data = await oracle_db.get_tables()
        tables = []
        for table_info in tables_data:
            details = await oracle_db.get_table_details(table_info["name"])
            tables.append(Table(
                name=details["name"],
                db_schema=table_info.get("schema", "dbo"),
                columns=details["columns"],
                primary_keys=[c["name"] for c in details["columns"] if c["is_primary_key"]],
                foreign_keys=details.get("foreign_keys", []),
            ))
        return tables
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tables/{table_name}", response_model=Table)
async def get_table(table_name: str):
    try:
        details = await oracle_db.get_table_details(table_name)
        return Table(
            name=details["name"],
            db_schema="dbo",
            columns=details["columns"],
            primary_keys=[c["name"] for c in details["columns"] if c["is_primary_key"]],
            foreign_keys=details.get("foreign_keys", []),
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Table {table_name} not found")


@router.get("/erd", response_model=ERDData)
async def get_erd():
    try:
        tables_data = await oracle_db.get_tables()
        
        nodes = []
        edges = []
        positions = {}
        
        for i, table_info in enumerate(tables_data):
            details = await oracle_db.get_table_details(table_info["name"])
            row = i // 4
            col = i % 4
            
            nodes.append(ERDNode(
                id=details["name"],
                type="table",
                position={"x": col * 300, "y": row * 250},
                data={"table": {
                    "name": details["name"],
                    "columns": details["columns"],
                    "primaryKeys": [c["name"] for c in details["columns"] if c["is_primary_key"]],
                    "foreignKeys": details.get("foreign_keys", []),
                }},
            ))
            
            for fk in details.get("foreign_keys", []):
                edges.append(ERDEdge(
                    id=f"edge-{details['name']}-{fk['referenced_table']}",
                    source=fk["referenced_table"],
                    target=details["name"],
                    label=fk["column"],
                    type="foreign",
                ))
        
        return ERDData(nodes=nodes, edges=edges)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/groups", response_model=list[SchemaGroup])
async def get_groups():
    return GROUPS


@router.post("/groups", response_model=SchemaGroup)
async def create_group(group: SchemaGroupCreate):
    new_group = SchemaGroup(
        id=str(len(GROUPS) + 1),
        name=group.name,
        color=group.color,
        table_names=group.table_names,
    )
    GROUPS.append(new_group)
    return new_group


@router.patch("/groups/{group_id}", response_model=SchemaGroup)
async def update_group(group_id: str, group: SchemaGroupCreate):
    for g in GROUPS:
        if g.id == group_id:
            g.name = group.name
            g.color = group.color
            g.table_names = group.table_names
            return g
    raise HTTPException(status_code=404, detail="Group not found")


@router.delete("/groups/{group_id}")
async def delete_group(group_id: str):
    global GROUPS
    GROUPS = [g for g in GROUPS if g.id != group_id]
    return {"message": "Group deleted"}
