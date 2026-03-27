from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from ..core.config import get_settings

settings = get_settings()

DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class VectorDB:
    """PostgreSQL with pgvector for schema embeddings"""
    
    def __init__(self):
        self._embedding_dim = 768  # nomic-embed-text dimension
    
    @contextmanager
    def get_connection(self):
        conn = engine.connect()
        try:
            yield conn
        finally:
            conn.close()
    
    def init_vector_extension(self) -> bool:
        """Enable pgvector extension"""
        with self.get_connection() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            return True
    
    def create_schema_embeddings_table(self) -> bool:
        """Create schema_embeddings table if not exists"""
        with self.get_connection() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS schema_embeddings (
                    id SERIAL PRIMARY KEY,
                    table_name VARCHAR(255) NOT NULL,
                    column_name VARCHAR(255),
                    description TEXT,
                    embedding vector(768),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(table_name, column_name)
                )
            """))
            
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_schema_embeddings 
                ON schema_embeddings USING ivfflat (embedding vector_cosine_ops)
                WITH (lists = 100)
            """))
            return True
    
    def insert_embedding(self, table_name: str, column_name: str, 
                        description: str, embedding: List[float]) -> bool:
        """Insert or update schema embedding"""
        with self.get_connection() as conn:
            embedding_str = f"[{','.join(map(str, embedding))}]"
            conn.execute(text("""
                INSERT INTO schema_embeddings (table_name, column_name, description, embedding)
                VALUES (:table_name, :column_name, :description, :embedding::vector)
                ON CONFLICT (table_name, column_name) 
                DO UPDATE SET description = EXCLUDED.description, 
                              embedding = EXCLUDED.embedding,
                              updated_at = CURRENT_TIMESTAMP
            """), {
                "table_name": table_name,
                "column_name": column_name,
                "description": description,
                "embedding": embedding_str
            })
            return True
    
    def semantic_search(self, query_embedding: List[float], 
                        top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar schema entries"""
        with self.get_connection() as conn:
            embedding_str = f"[{','.join(map(str, query_embedding))}]"
            result = conn.execute(text("""
                SELECT table_name, column_name, description,
                       1 - (embedding <=> :query_embedding::vector) as similarity
                FROM schema_embeddings
                ORDER BY embedding <=> :query_embedding::vector
                LIMIT :top_k
            """), {"query_embedding": embedding_str, "top_k": top_k})
            
            return [
                {
                    "table_name": row[0],
                    "column_name": row[1],
                    "description": row[2],
                    "similarity": float(row[3])
                }
                for row in result.fetchall()
            ]
    
    def get_all_embeddings(self) -> List[Dict[str, Any]]:
        """Get all schema embeddings"""
        with self.get_connection() as conn:
            result = conn.execute(text("""
                SELECT id, table_name, column_name, description, created_at, updated_at
                FROM schema_embeddings
                ORDER BY table_name
            """))
            return [
                {
                    "id": row[0],
                    "table_name": row[1],
                    "column_name": row[2],
                    "description": row[3],
                    "created_at": row[4],
                    "updated_at": row[5]
                }
                for row in result.fetchall()
            ]
    
    def get_table_embeddings(self, table_name: str) -> List[Dict[str, Any]]:
        """Get embeddings for a specific table"""
        with self.get_connection() as conn:
            result = conn.execute(text("""
                SELECT id, column_name, description, embedding
                FROM schema_embeddings
                WHERE table_name = :table_name
            """), {"table_name": table_name})
            return [
                {
                    "id": row[0],
                    "column_name": row[1],
                    "description": row[2],
                    "embedding": row[3]
                }
                for row in result.fetchall()
            ]
    
    def delete_embedding(self, table_name: str, column_name: str = None) -> bool:
        """Delete embeddings for a table or column"""
        with self.get_connection() as conn:
            if column_name:
                conn.execute(text("""
                    DELETE FROM schema_embeddings 
                    WHERE table_name = :table_name AND column_name = :column_name
                """), {"table_name": table_name, "column_name": column_name})
            else:
                conn.execute(text("""
                    DELETE FROM schema_embeddings WHERE table_name = :table_name
                """), {"table_name": table_name})
            return True
    
    def delete_all_embeddings(self) -> bool:
        """Delete all embeddings"""
        with self.get_connection() as conn:
            conn.execute(text("DELETE FROM schema_embeddings"))
            return True
    
    def get_embedding_count(self) -> int:
        """Get total number of embeddings"""
        with self.get_connection() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM schema_embeddings"))
            return result.fetchone()[0]
    
    def get_tables_count(self) -> int:
        """Get number of unique tables with embeddings"""
        with self.get_connection() as conn:
            result = conn.execute(text("SELECT COUNT(DISTINCT table_name) FROM schema_embeddings"))
            return result.fetchone()[0]


# Query history operations
class QueryHistoryDB:
    """Query history storage"""
    
    def add_query(self, user_id: str, natural_language: str, 
                  generated_sql: str, success: bool = True, 
                  execution_time_ms: int = 0) -> bool:
        """Add query to history"""
        with VectorDB().get_connection() as conn:
            conn.execute(text("""
                INSERT INTO query_history 
                (user_id, natural_language, generated_sql, success, execution_time_ms)
                VALUES (:user_id, :nl, :sql, :success, :exec_time)
            """), {
                "user_id": user_id,
                "nl": natural_language,
                "sql": generated_sql,
                "success": success,
                "exec_time": execution_time_ms
            })
            return True
    
    def get_history(self, user_id: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get query history"""
        with VectorDB().get_connection() as conn:
            if user_id:
                result = conn.execute(text("""
                    SELECT id, user_id, natural_language, generated_sql, 
                           success, execution_time_ms, created_at
                    FROM query_history
                    WHERE user_id = :user_id
                    ORDER BY created_at DESC
                    LIMIT :limit
                """), {"user_id": user_id, "limit": limit})
            else:
                result = conn.execute(text("""
                    SELECT id, user_id, natural_language, generated_sql, 
                           success, execution_time_ms, created_at
                    FROM query_history
                    ORDER BY created_at DESC
                    LIMIT :limit
                """), {"limit": limit})
            
            return [
                {
                    "id": row[0],
                    "user_id": row[1],
                    "natural_language": row[2],
                    "generated_sql": row[3],
                    "success": row[4],
                    "execution_time_ms": row[5],
                    "created_at": row[6]
                }
                for row in result.fetchall()
            ]


vector_db = VectorDB()
query_history_db = QueryHistoryDB()
