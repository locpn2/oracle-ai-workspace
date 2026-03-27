import oracledb
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Optional
from ..core.config import get_settings

settings = get_settings()


class OracleConnection:
    def __init__(self):
        self.pool: Optional[oracledb.SessionPool] = None

    def connect(self):
        if not self.pool:
            dsn = f"{settings.oracle_host}:{settings.oracle_port}/{settings.oracle_service}"
            self.pool = oracledb.create_pool(
                user=settings.oracle_user,
                password=settings.oracle_password,
                dsn=dsn,
                min=2,
                max=10,
                increment=1,
            )
        return self.pool

    @contextmanager
    def get_connection(self):
        pool = self.connect()
        conn = pool.acquire()
        try:
            yield conn
        finally:
            pool.release(conn)

    @contextmanager
    def get_session(self) -> Session:
        pool = self.connect()
        conn = pool.acquire()
        try:
            yield conn
        finally:
            pool.release(conn)

    async def get_tables(self) -> list[dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT table_name, owner
                FROM all_tables
                WHERE owner = :owner
                ORDER BY table_name
            """, {"owner": settings.oracle_user.upper()})
            return [{"name": row[0], "schema": row[1]} for row in cursor.fetchall()]

    async def get_table_details(self, table_name: str) -> dict:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get columns
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
            
            # Get foreign keys
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

    async def execute_query(self, sql: str, page: int = 1, page_size: int = 100):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get total count
            count_sql = f"SELECT COUNT(*) FROM ({sql})"
            cursor.execute(count_sql)
            total_rows = cursor.fetchone()[0]
            
            # Get paginated results
            offset = (page - 1) * page_size
            paginated_sql = f"""
                SELECT * FROM (
                    SELECT a.*, ROWNUM rnum FROM ({sql}) a WHERE ROWNUM <= :max_row
                ) WHERE rnum > :min_row
            """
            cursor.execute(paginated_sql, {"max_row": offset + page_size, "min_row": offset})
            
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return {
                "columns": columns,
                "rows": rows,
                "total_rows": total_rows,
                "page": page,
                "page_size": page_size,
            }


oracle_db = OracleConnection()
