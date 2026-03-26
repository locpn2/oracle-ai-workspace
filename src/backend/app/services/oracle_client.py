import oracledb
from typing import Optional, Dict, List, Any, Tuple
from contextlib import contextmanager
from dataclasses import dataclass
from app.config import get_settings

settings = get_settings()


@dataclass
class OracleConnectionConfig:
    host: str
    port: int
    username: str
    password: str
    service_name: Optional[str] = None
    sid: Optional[str] = None
    connection_type: str = "service_name"


class OracleClient:
    def __init__(self, config: OracleConnectionConfig):
        self.config = config
        self._pool: Optional[oracledb.SessionPool] = None
    
    def _get_dsn(self) -> str:
        if self.config.connection_type == "sid":
            return oracledb.makedsn(
                self.config.host,
                self.config.port,
                sid=self.config.sid
            )
        return oracledb.makedsn(
            self.config.host,
            self.config.port,
            service_name=self.config.service_name
        )
    
    def connect(self) -> oracledb.Connection:
        if settings.ORACLE_CLIENT_PATH:
            oracledb.init_oracle_client(lib_dir=settings.ORACLE_CLIENT_PATH)
        
        return oracledb.connect(
            user=self.config.username,
            password=self.config.password,
            dsn=self._get_dsn()
        )
    
    @contextmanager
    def get_connection(self):
        conn = self.connect()
        try:
            yield conn
        finally:
            conn.close()
    
    def test_connection(self) -> Tuple[bool, str, Optional[str]]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT BANNER FROM V$VERSION WHERE ROWNUM = 1")
                version = cursor.fetchone()[0]
                cursor.close()
                return True, "Connection successful", version
        except Exception as e:
            return False, f"Connection failed: {str(e)}", None
    
    def get_schemas(self) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT OWNER 
                FROM ALL_TABLES 
                WHERE OWNER NOT IN ('SYS', 'SYSTEM', 'OUTLN', 'DIP', 'ORACLE_OCM', 
                                   'XS$NULL', 'MDDATA', 'CTXSYS', 'DVSYS', 'GSMADMIN_INTERNAL',
                                   'LBACSYS', 'MDSYS', 'OLAPSYS', 'ORDDATA', 'ORDSYS',
                                   'SI_INFORMTN_SCHEMA', 'SPATIAL_CSW_ADMIN_USR', 'SPATIAL_WFS_ADMIN_USR',
                                   'WMSYS', 'XDB', 'APPQOSSYS')
                ORDER BY OWNER
            """)
            schemas = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return schemas
    
    def get_tables(self, schema: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT TABLE_NAME, NUM_ROWS
                FROM ALL_TABLES
                WHERE OWNER = :schema
                ORDER BY TABLE_NAME
            """, {"schema": schema})
            tables = [
                {"name": row[0], "row_count": row[1]}
                for row in cursor.fetchall()
            ]
            cursor.close()
            return tables
    
    def get_columns(self, schema: str, table: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    DATA_LENGTH,
                    DATA_PRECISION,
                    DATA_SCALE,
                    NULLABLE,
                    DATA_DEFAULT,
                    CHAR_LENGTH
                FROM ALL_TAB_COLUMNS
                WHERE OWNER = :schema AND TABLE_NAME = :table
                ORDER BY COLUMN_ID
            """, {"schema": schema, "table": table})
            
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    "name": row[0],
                    "data_type": row[1],
                    "character_max_length": row[6] if row[1] in ('VARCHAR', 'CHAR', 'NVARCHAR2', 'NCHAR') else row[2],
                    "numeric_precision": row[3],
                    "numeric_scale": row[4],
                    "nullable": row[5] == 'Y',
                    "default_value": str(row[6]) if row[6] else None
                })
            cursor.close()
            return columns
    
    def get_primary_keys(self, schema: str, table: str) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COLUMN_NAME
                FROM ALL_CONS_COLUMNS
                WHERE OWNER = :schema
                  AND TABLE_NAME = :table
                  AND CONSTRAINT_NAME IN (
                      SELECT CONSTRAINT_NAME
                      FROM ALL_CONSTRAINTS
                      WHERE OWNER = :schema
                        AND TABLE_NAME = :table
                        AND CONSTRAINT_TYPE = 'P'
                  )
                ORDER BY POSITION
            """, {"schema": schema, "table": table})
            pks = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return pks
    
    def get_foreign_keys(self, schema: str, table: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    a.CONSTRAINT_NAME,
                    a.COLUMN_NAME,
                    c.OWNER AS REF_OWNER,
                    c.TABLE_NAME AS REF_TABLE,
                    cc.COLUMN_NAME AS REF_COLUMN,
                    c.DELETE_RULE
                FROM ALL_CONS_COLUMNS a
                JOIN ALL_CONSTRAINTS c ON a.CONSTRAINT_NAME = c.CONSTRAINT_NAME AND a.OWNER = c.OWNER
                JOIN ALL_CONS_COLUMNS cc ON c.CONSTRAINT_NAME = cc.CONSTRAINT_NAME AND c.OWNER = cc.OWNER
                WHERE a.OWNER = :schema
                  AND a.TABLE_NAME = :table
                  AND c.CONSTRAINT_TYPE = 'R'
                  AND cc.POSITION = a.POSITION
                ORDER BY a.CONSTRAINT_NAME, a.POSITION
            """, {"schema": schema, "table": table})
            
            fks = {}
            for row in cursor.fetchall():
                constraint_name = row[0]
                if constraint_name not in fks:
                    fks[constraint_name] = {
                        "name": constraint_name,
                        "columns": [],
                        "referenced_schema": row[2],
                        "referenced_table": row[3],
                        "referenced_columns": [],
                        "delete_rule": row[5]
                    }
                fks[constraint_name]["columns"].append(row[1])
                fks[constraint_name]["referenced_columns"].append(row[4])
            
            cursor.close()
            return list(fks.values())
    
    def get_indexes(self, schema: str, table: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    INDEX_NAME,
                    INDEX_TYPE,
                    UNIQUENESS,
                    STATUS
                FROM ALL_INDEXES
                WHERE OWNER = :schema AND TABLE_NAME = :table
                ORDER BY INDEX_NAME
            """, {"schema": schema, "table": table})
            
            indexes = {}
            for row in cursor.fetchall():
                indexes[row[0]] = {
                    "name": row[0],
                    "index_type": row[1],
                    "uniqueness": row[2],
                    "status": row[3],
                    "columns": []
                }
            
            cursor.execute("""
                SELECT 
                    INDEX_NAME,
                    COLUMN_NAME,
                    COLUMN_POSITION
                FROM ALL_IND_COLUMNS
                WHERE INDEX_OWNER = :schema AND TABLE_NAME = :table
                ORDER BY INDEX_NAME, COLUMN_POSITION
            """, {"schema": schema, "table": table})
            
            for row in cursor.fetchall():
                if row[0] in indexes:
                    indexes[row[0]]["columns"].append(row[1])
            
            cursor.close()
            return list(indexes.values())
    
    def execute_query(self, sql: str, params: Optional[Dict] = None, fetch_size: int = 100) -> Tuple[bool, List[str], List[Tuple], Optional[str]]:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(sql, params)
                else:
                    cursor.execute(sql)
                
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                rows = cursor.fetchmany(fetch_size)
                cursor.close()
                return True, columns, rows, None
        except Exception as e:
            return False, [], [], str(e)
    
    def get_table_data(self, schema: str, table: str, limit: int = 1000, offset: int = 0) -> Tuple[List[str], List[Tuple]]:
        sql = f'SELECT * FROM "{schema}"."{table}" WHERE ROWNUM <= :limit OFFSET :offset'
        success, columns, rows, _ = self.execute_query(sql, {"limit": limit, "offset": offset})
        return columns, rows
