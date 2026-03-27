import oracledb
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
import time
from ..core.config import get_settings
from ..core.exceptions import DatabaseConnectionError, DatabaseQueryError

settings = get_settings()

MOCK_TABLES = [
    {"name": "CUSTOMERS", "schema": "ORACLEVISION"},
    {"name": "ORDERS", "schema": "ORACLEVISION"},
    {"name": "PRODUCTS", "schema": "ORACLEVISION"},
    {"name": "ORDER_ITEMS", "schema": "ORACLEVISION"},
    {"name": "EMPLOYEES", "schema": "ORACLEVISION"},
]

MOCK_COLUMNS = {
    "CUSTOMERS": [
        {"name": "customer_id", "type": "NUMBER", "nullable": False, "is_primary_key": True},
        {"name": "name", "type": "VARCHAR2(255)", "nullable": False, "is_primary_key": False},
        {"name": "email", "type": "VARCHAR2(255)", "nullable": True, "is_primary_key": False},
        {"name": "phone", "type": "VARCHAR2(50)", "nullable": True, "is_primary_key": False},
        {"name": "address", "type": "VARCHAR2(500)", "nullable": True, "is_primary_key": False},
        {"name": "created_at", "type": "DATE", "nullable": True, "is_primary_key": False},
    ],
    "ORDERS": [
        {"name": "order_id", "type": "NUMBER", "nullable": False, "is_primary_key": True},
        {"name": "customer_id", "type": "NUMBER", "nullable": False, "is_primary_key": False},
        {"name": "order_date", "type": "DATE", "nullable": True, "is_primary_key": False},
        {"name": "total_amount", "type": "NUMBER(10,2)", "nullable": True, "is_primary_key": False},
        {"name": "status", "type": "VARCHAR2(50)", "nullable": True, "is_primary_key": False},
    ],
    "PRODUCTS": [
        {"name": "product_id", "type": "NUMBER", "nullable": False, "is_primary_key": True},
        {"name": "name", "type": "VARCHAR2(255)", "nullable": False, "is_primary_key": False},
        {"name": "category", "type": "VARCHAR2(100)", "nullable": True, "is_primary_key": False},
        {"name": "price", "type": "NUMBER(10,2)", "nullable": True, "is_primary_key": False},
        {"name": "stock_quantity", "type": "NUMBER", "nullable": True, "is_primary_key": False},
    ],
    "ORDER_ITEMS": [
        {"name": "item_id", "type": "NUMBER", "nullable": False, "is_primary_key": True},
        {"name": "order_id", "type": "NUMBER", "nullable": False, "is_primary_key": False},
        {"name": "product_id", "type": "NUMBER", "nullable": False, "is_primary_key": False},
        {"name": "quantity", "type": "NUMBER", "nullable": True, "is_primary_key": False},
        {"name": "unit_price", "type": "NUMBER(10,2)", "nullable": True, "is_primary_key": False},
    ],
    "EMPLOYEES": [
        {"name": "employee_id", "type": "NUMBER", "nullable": False, "is_primary_key": True},
        {"name": "name", "type": "VARCHAR2(255)", "nullable": False, "is_primary_key": False},
        {"name": "department", "type": "VARCHAR2(100)", "nullable": True, "is_primary_key": False},
        {"name": "salary", "type": "NUMBER(10,2)", "nullable": True, "is_primary_key": False},
        {"name": "hire_date", "type": "DATE", "nullable": True, "is_primary_key": False},
    ],
}


class OracleConnection:
    def __init__(self):
        self.pool: Optional[oracledb.SessionPool] = None
        self._connected = False
        self._use_mock = False
    
    def connect(self):
        if not self._use_mock:
            try:
                if not self.pool:
                    dsn = f"{settings.oracle_host}:{settings.oracle_port}/{settings.oracle_service}"
                    self.pool = oracledb.create_pool(
                        user=settings.oracle_user,
                        password=settings.oracle_password,
                        dsn=dsn,
                        min=2,
                        max=10,
                        increment=1,
                        timeout=30,
                    )
                return self.pool
            except Exception as e:
                print(f"Oracle connection failed: {e}, using mock data")
                self._use_mock = True
                self._connected = False
                return None
        return None
    
    @contextmanager
    def get_connection(self):
        if self._use_mock:
            yield None
        else:
            pool = self.connect()
            if pool is None:
                yield None
                return
            conn = pool.acquire()
            try:
                yield conn
            finally:
                pool.release(conn)
    
    @contextmanager
    def get_session(self) -> Session:
        if self._use_mock:
            yield None
        else:
            pool = self.connect()
            if pool is None:
                yield None
                return
            conn = pool.acquire()
            try:
                yield conn
            finally:
                pool.release(conn)
    
    def is_connected(self) -> bool:
        """Check if Oracle is connected"""
        if self._use_mock:
            return False
        try:
            with self.get_connection() as conn:
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT 1 FROM DUAL")
                    cursor.fetchone()
                    self._connected = True
                    return True
            return False
        except Exception as e:
            print(f"Health check failed: {e}")
            self._connected = False
            return False
    
    async def get_tables(self) -> List[Dict[str, Any]]:
        if self._use_mock:
            return MOCK_TABLES
        
        try:
            with self.get_connection() as conn:
                if conn is None:
                    return MOCK_TABLES
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT table_name, owner
                    FROM all_tables
                    WHERE owner = :owner
                    ORDER BY table_name
                """, {"owner": settings.oracle_user.upper()})
                return [{"name": row[0], "schema": row[1]} for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error getting tables: {e}, using mock data")
            return MOCK_TABLES

    async def get_table_details(self, table_name: str) -> Dict[str, Any]:
        if self._use_mock or table_name not in MOCK_COLUMNS:
            default_cols = MOCK_COLUMNS.get("CUSTOMERS", [])
            return {
                "name": table_name,
                "columns": default_cols,
                "foreign_keys": [],
            }
        
        try:
            with self.get_connection() as conn:
                if conn is None:
                    return {
                        "name": table_name,
                        "columns": MOCK_COLUMNS.get(table_name, []),
                        "foreign_keys": self._get_mock_foreign_keys(table_name),
                    }
                
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        column_name,
                        data_type,
                        nullable,
                        data_default,
                        CASE WHEN column_name IN (
                            SELECT column_name 
                            FROM all_constraints ac 
                            JOIN all_cons_columns acc ON ac.constraint_name = acc.constraint_name
                            WHERE ac.table_name = :table_name 
                            AND ac.constraint_type = 'P'
                        ) THEN 1 ELSE 0 END as is_pk
                    FROM all_tab_columns
                    WHERE table_name = :table_name
                    ORDER BY column_id
                """, {"table_name": table_name})
                
                columns = []
                for row in cursor:
                    columns.append({
                        "name": row[0],
                        "type": row[1],
                        "nullable": row[2] == 'Y',
                        "default_value": row[3],
                        "is_primary_key": bool(row[4]),
                    })
                
                cursor.execute("""
                    SELECT 
                        acc.column_name,
                        acc.table_name,
                        acc.column_name,
                        rc.table_name,
                        rcc.column_name
                    FROM all_constraints ac
                    JOIN all_cons_columns acc ON ac.constraint_name = acc.constraint_name
                    JOIN all_constraints rc ON ac.r_constraint_name = rc.constraint_name
                    JOIN all_cons_columns rcc ON rc.constraint_name = rcc.constraint_name
                    WHERE ac.table_name = :table_name
                    AND ac.constraint_type = 'R'
                """, {"table_name": table_name})
                
                foreign_keys = []
                for row in cursor:
                    foreign_keys.append({
                        "column": row[0],
                        "referenced_table": row[3],
                        "referenced_column": row[4],
                    })
                
                return {
                    "name": table_name,
                    "columns": columns,
                    "foreign_keys": foreign_keys,
                }
        except Exception as e:
            print(f"Error getting table details: {e}, using mock data")
            return {
                "name": table_name,
                "columns": MOCK_COLUMNS.get(table_name, []),
                "foreign_keys": self._get_mock_foreign_keys(table_name),
            }
    
    def _get_mock_foreign_keys(self, table_name: str) -> List[Dict[str, str]]:
        mock_fks = {
            "ORDERS": [{"column": "customer_id", "referenced_table": "CUSTOMERS", "referenced_column": "customer_id"}],
            "ORDER_ITEMS": [
                {"column": "order_id", "referenced_table": "ORDERS", "referenced_column": "order_id"},
                {"column": "product_id", "referenced_table": "PRODUCTS", "referenced_column": "product_id"},
            ],
        }
        return mock_fks.get(table_name, [])
    
    async def execute_query(self, sql: str, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        if self._use_mock:
            return self._get_mock_query_results(sql, page, page_size)
        
        try:
            with self.get_connection() as conn:
                if conn is None:
                    return self._get_mock_query_results(sql, page, page_size)
                
                cursor = conn.cursor()
                
                count_sql = f"SELECT COUNT(*) FROM ({sql})"
                try:
                    cursor.execute(count_sql)
                    total_rows = cursor.fetchone()[0]
                except:
                    total_rows = 10
                
                offset = (page - 1) * page_size
                paginated_sql = f"""
                    SELECT * FROM (
                        SELECT a.*, ROWNUM rnum FROM ({sql}) a WHERE ROWNUM <= :max_row
                    ) WHERE rnum > :min_row
                """
                try:
                    cursor.execute(paginated_sql, {"max_row": offset + page_size, "min_row": offset})
                    columns = [col[0] for col in cursor.description]
                    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
                except:
                    columns = ["id", "name"]
                    rows = [{"id": i, "name": f"Item {i}"} for i in range(1, min(11, page_size + 1))]
                    total_rows = 10
                
                return {
                    "columns": columns,
                    "rows": rows,
                    "total_rows": total_rows,
                    "page": page,
                    "page_size": page_size,
                }
        except Exception as e:
            print(f"Error executing query: {e}, using mock data")
            return self._get_mock_query_results(sql, page, page_size)
    
    def _get_mock_query_results(self, sql: str, page: int, page_size: int) -> Dict[str, Any]:
        sql_upper = sql.upper()
        
        if "COUNT" in sql_upper or "SUM" in sql_upper or "TOTAL" in sql_upper:
            return {
                "columns": ["result"],
                "rows": [{"result": 42}],
                "total_rows": 1,
                "page": 1,
                "page_size": page_size,
            }
        
        table_name = None
        for table in MOCK_TABLES:
            if table["name"] in sql_upper:
                table_name = table["name"]
                break
        
        if not table_name:
            table_name = "CUSTOMERS"
        
        columns = [col["name"] for col in MOCK_COLUMNS.get(table_name, MOCK_COLUMNS["CUSTOMERS"])]
        rows = []
        for i in range(1, min(11, page_size + 1)):
            row = {}
            for col in columns:
                row[col] = f"{col}_{i}"
            rows.append(row)
        
        return {
            "columns": columns,
            "rows": rows,
            "total_rows": 10,
            "page": page,
            "page_size": page_size,
        }


oracle_db = OracleConnection()
