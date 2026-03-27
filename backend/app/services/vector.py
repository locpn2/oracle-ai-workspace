from typing import List, Dict, Any, Optional
from datetime import datetime
from ..db.postgres import vector_db
from ..db.oracle import oracle_db
from ..llm.ollama import ollama_client


class SyncStatus:
    def __init__(self):
        self.last_sync: Optional[datetime] = None
        self.status: str = "idle"  # idle, syncing, completed, error
        self.tables_synced: int = 0
        self.total_tables: int = 0
        self.error: Optional[str] = None


sync_status = SyncStatus()


class VectorService:
    """Service for managing vector embeddings and semantic search"""
    
    def __init__(self):
        self.vector_db = vector_db
    
    async def init(self) -> bool:
        """Initialize vector DB with required tables"""
        try:
            self.vector_db.init_vector_extension()
            self.vector_db.create_schema_embeddings_table()
            return True
        except Exception as e:
            print(f"Error initializing vector DB: {e}")
            return False
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text using Ollama"""
        try:
            return await ollama_client.embed(text)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return []
    
    async def embed_table_info(self, table_name: str) -> Dict[str, Any]:
        """Generate embeddings for table and its columns"""
        try:
            table_details = await oracle_db.get_table_details(table_name)
            
            table_description = f"Table: {table_name}\n"
            table_description += f"Columns: {', '.join([c['name'] for c in table_details['columns']])}\n"
            table_description += f"Primary Keys: {', '.join([c['name'] for c in table_details['columns'] if c.get('is_primary_key')])}\n"
            if table_details.get('foreign_keys'):
                fk_list = [f"{fk['column']} -> {fk['referenced_table']}.{fk['referenced_column']}" for fk in table_details['foreign_keys']]
            table_description += f"Foreign Keys: {', '.join(fk_list)}"
            
            table_embedding = await self.embed_text(table_description)
            
            column_embeddings = []
            for col in table_details['columns']:
                col_description = f"Table: {table_name}, Column: {col['name']}, Type: {col['type']}, Nullable: {col.get('nullable', True)}"
                if col.get('is_primary_key'):
                    col_description += ", Primary Key"
                
                col_embedding = await self.embed_text(col_description)
                column_embeddings.append({
                    "column_name": col['name'],
                    "description": col_description,
                    "embedding": col_embedding
                })
            
            return {
                "table_name": table_name,
                "table_embedding": table_embedding,
                "table_description": table_description,
                "columns": column_embeddings
            }
        except Exception as e:
            print(f"Error embedding table {table_name}: {e}")
            return {}
    
    async def sync_full_schema(self) -> Dict[str, Any]:
        """Sync all tables from Oracle to pgvector"""
        global sync_status
        
        try:
            sync_status.status = "syncing"
            sync_status.error = None
            
            tables = await oracle_db.get_tables()
            sync_status.total_tables = len(tables)
            sync_status.tables_synced = 0
            
            for table_info in tables:
                try:
                    table_name = table_info["name"]
                    embedding_data = await self.embed_table_info(table_name)
                    
                    if embedding_data and embedding_data.get("table_embedding"):
                        self.vector_db.insert_embedding(
                            table_name=table_name,
                            column_name=None,
                            description=embedding_data["table_description"],
                            embedding=embedding_data["table_embedding"]
                        )
                        
                        for col in embedding_data.get("columns", []):
                            if col.get("embedding"):
                                self.vector_db.insert_embedding(
                                    table_name=table_name,
                                    column_name=col["column_name"],
                                    description=col["description"],
                                    embedding=col["embedding"]
                                )
                        
                        sync_status.tables_synced += 1
                except Exception as e:
                    print(f"Error syncing table {table_info['name']}: {e}")
                    continue
            
            sync_status.last_sync = datetime.now()
            sync_status.status = "completed"
            
            return {
                "success": True,
                "tables_synced": sync_status.tables_synced,
                "total_tables": sync_status.total_tables,
                "last_sync": sync_status.last_sync.isoformat() if sync_status.last_sync else None
            }
        except Exception as e:
            sync_status.status = "error"
            sync_status.error = str(e)
            return {
                "success": False,
                "error": str(e)
            }
    
    async def sync_table(self, table_name: str) -> bool:
        """Sync a single table to pgvector"""
        try:
            embedding_data = await self.embed_table_info(table_name)
            
            if not embedding_data:
                return False
            
            if embedding_data.get("table_embedding"):
                self.vector_db.insert_embedding(
                    table_name=table_name,
                    column_name=None,
                    description=embedding_data["table_description"],
                    embedding=embedding_data["table_embedding"]
                )
            
            for col in embedding_data.get("columns", []):
                if col.get("embedding"):
                    self.vector_db.insert_embedding(
                        table_name=table_name,
                        column_name=col["column_name"],
                        description=col["description"],
                        embedding=col["embedding"]
                    )
            
            return True
        except Exception as e:
            print(f"Error syncing table {table_name}: {e}")
            return False
    
    async def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search schema using semantic similarity"""
        try:
            query_embedding = await self.embed_text(query)
            
            if not query_embedding:
                return []
            
            results = self.vector_db.semantic_search(query_embedding, top_k)
            return results
        except Exception as e:
            print(f"Error in semantic search: {e}")
            return []
    
    def get_sync_status(self) -> Dict[str, Any]:
        """Get current sync status"""
        return {
            "last_sync": sync_status.last_sync.isoformat() if sync_status.last_sync else None,
            "status": sync_status.status,
            "tables_synced": sync_status.tables_synced,
            "total_tables": sync_status.total_tables,
            "error": sync_status.error
        }
    
    def clear_all_embeddings(self) -> bool:
        """Clear all embeddings from vector store"""
        try:
            self.vector_db.delete_all_embeddings()
            sync_status.last_sync = None
            sync_status.tables_synced = 0
            sync_status.total_tables = 0
            sync_status.status = "idle"
            return True
        except Exception as e:
            print(f"Error clearing embeddings: {e}")
            return False
    
    def get_schema_context(self, table_names: List[str] = None) -> str:
        """Get schema context for LLM from stored embeddings"""
        try:
            if table_names:
                context_parts = []
                for table_name in table_names:
                    embeddings = self.vector_db.get_table_embeddings(table_name)
                    if embeddings:
                        table_info = f"Table: {table_name}\n"
                        for emb in embeddings:
                            if emb.get("column_name"):
                                table_info += f"  - {emb['description']}\n"
                            else:
                                table_info = f"Table: {table_name}\nDescription: {emb.get('description', '')}\n"
                        context_parts.append(table_info)
                return "\n\n".join(context_parts) if context_parts else ""
            else:
                all_embeddings = self.vector_db.get_all_embeddings()
                
                table_contexts = {}
                for emb in all_embeddings:
                    table = emb.get("table_name")
                    if table not in table_contexts:
                        table_contexts[table] = {"description": "", "columns": []}
                    
                    if emb.get("column_name"):
                        table_contexts[table]["columns"].append(emb.get("description", ""))
                    else:
                        table_contexts[table]["description"] = emb.get("description", "")
                
                context_parts = []
                for table, info in table_contexts.items():
                    ctx = f"Table: {table}\n"
                    if info["description"]:
                        ctx += f"Description: {info['description']}\n"
                    if info["columns"]:
                        ctx += f"Columns: {', '.join(info['columns'][:5])}"
                    context_parts.append(ctx)
                
                return "\n\n".join(context_parts)
        except Exception as e:
            print(f"Error getting schema context: {e}")
            return ""


vector_service = VectorService()