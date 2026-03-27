from pydantic import BaseModel
from typing import Optional


class Column(BaseModel):
    name: str
    type: str
    nullable: bool = True
    default_value: Optional[str] = None
    is_primary_key: bool = False


class ForeignKey(BaseModel):
    column: str
    referenced_table: str
    referenced_column: str


class Table(BaseModel):
    name: str
    db_schema: str = "dbo"
    columns: list[Column] = []
    primary_keys: list[str] = []
    foreign_keys: list[ForeignKey] = []
    row_count: Optional[int] = None


class ERDNode(BaseModel):
    id: str
    type: str = "table"
    position: dict = {"x": 0, "y": 0}
    data: dict = {}


class ERDEdge(BaseModel):
    id: str
    source: str
    target: str
    label: Optional[str] = None
    type: str = "primary"


class ERDData(BaseModel):
    nodes: list[ERDNode] = []
    edges: list[ERDEdge] = []


class SchemaGroup(BaseModel):
    id: str
    name: str
    color: str
    table_names: list[str] = []


class SchemaGroupCreate(BaseModel):
    name: str
    color: str
    table_names: list[str] = []
