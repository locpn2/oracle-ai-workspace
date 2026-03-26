import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid
from app.config import get_settings
from app.services.ai_service import EmbeddingService

settings = get_settings()


class VectorService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.chroma_client = None
        self._init_chroma()
    
    def _init_chroma(self):
        try:
            self.chroma_client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
        except Exception as e:
            print(f"Warning: Could not initialize ChromaDB: {e}")
            self.chroma_client = None
    
    def create_collection(self, name: str, dimension: int = None) -> Optional[str]:
        if not self.chroma_client:
            return None
        
        if dimension is None:
            dimension = settings.EMBEDDING_DIMENSION
        
        try:
            collection = self.chroma_client.create_collection(
                name=name,
                metadata={"dimension": dimension}
            )
            return collection.name
        except Exception as e:
            existing = self.get_collection(name)
            if existing:
                return existing
            raise e
    
    def get_collection(self, name: str):
        if not self.chroma_client:
            return None
        
        try:
            return self.chroma_client.get_collection(name)
        except:
            return None
    
    def list_collections(self) -> List[Dict[str, Any]]:
        if not self.chroma_client:
            return []
        
        try:
            collections = self.chroma_client.list_collections()
            return [
                {
                    "name": c.name,
                    "metadata": c.metadata,
                    "count": c.count()
                }
                for c in collections
            ]
        except Exception as e:
            return []
    
    def delete_collection(self, name: str) -> bool:
        if not self.chroma_client:
            return False
        
        try:
            self.chroma_client.delete_collection(name)
            return True
        except:
            return False
    
    def add_vectors(
        self,
        collection_name: str,
        documents: List[str],
        embeddings: List[List[float]] = None,
        metadatas: List[Dict[str, Any]] = None,
        ids: List[str] = None
    ) -> bool:
        collection = self.get_collection(collection_name)
        if not collection:
            return False
        
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        if embeddings is None:
            embeddings = self.embedding_service.get_embeddings_batch(documents)
        
        try:
            collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            return True
        except Exception as e:
            print(f"Error adding vectors: {e}")
            return False
    
    def search(
        self,
        collection_name: str,
        query: str,
        top_k: int = 5,
        filter_metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        collection = self.get_collection(collection_name)
        if not collection:
            return []
        
        try:
            query_embedding = self.embedding_service.get_embedding(query)
            
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_metadata,
                include=["documents", "metadatas", "distances"]
            )
            
            search_results = []
            if results and "documents" in results:
                for i, doc in enumerate(results["documents"][0]):
                    search_results.append({
                        "id": results["ids"][0][i] if "ids" in results else str(i),
                        "document": doc,
                        "metadata": results["metadatas"][0][i] if "metadatas" in results and results["metadatas"] else {},
                        "score": 1 - results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
                    })
            
            return search_results
        except Exception as e:
            print(f"Error searching: {e}")
            return []
    
    def vectorize_table(
        self,
        collection_name: str,
        table_data: List[Dict[str, Any]],
        columns: List[str],
        text_columns: List[str],
        primary_key_column: str = None,
        batch_size: int = 100
    ) -> Tuple[int, int]:
        if not table_data:
            return 0, 0
        
        collection = self.get_collection(collection_name)
        if not collection:
            collection_name = self.create_collection(collection_name)
            if not collection_name:
                return 0, 0
        
        total_embedded = 0
        total_failed = 0
        
        for i in range(0, len(table_data), batch_size):
            batch = table_data[i:i + batch_size]
            documents = []
            metadatas = []
            ids = []
            
            for row in batch:
                doc = self.embedding_service.text_to_vector_record(row, columns, text_columns)
                documents.append(doc)
                
                metadata = {
                    "source_table": collection_name,
                    "row_data": str(row)
                }
                
                if primary_key_column and primary_key_column in row:
                    metadata["primary_key"] = str(row[primary_key_column])
                
                metadatas.append(metadata)
                
                if primary_key_column and primary_key_column in row:
                    ids.append(f"{collection_name}_{row[primary_key_column]}")
                else:
                    ids.append(f"{collection_name}_{uuid.uuid4()}")
            
            try:
                success = self.add_vectors(
                    collection_name=collection_name,
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                if success:
                    total_embedded += len(documents)
                else:
                    total_failed += len(documents)
            except Exception as e:
                total_failed += len(batch)
                print(f"Batch embedding error: {e}")
        
        return total_embedded, total_failed
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        collection = self.get_collection(collection_name)
        if not collection:
            return {"error": "Collection not found"}
        
        return {
            "name": collection.name,
            "count": collection.count(),
            "metadata": collection.metadata
        }
    
    def reset(self) -> bool:
        if not self.chroma_client:
            return False
        
        try:
            self.chroma_client.reset()
            return True
        except Exception as e:
            return False
