from typing import Optional, List, Dict, Any, Tuple
from app.config import get_settings

settings = get_settings()


class AIService:
    def __init__(self):
        self.llm_provider = settings.LLM_PROVIDER
        self.llm_model = settings.LLM_MODEL
        self.openai_client = None
        self.anthropic_client = None
        
        self._init_clients()
    
    def _init_clients(self):
        try:
            if self.llm_provider == "openai" and settings.OPENAI_API_KEY:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        except Exception:
            pass
        
        try:
            if settings.ANTHROPIC_API_KEY:
                from anthropic import Anthropic
                self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        except Exception:
            pass
    
    def generate_sql(
        self,
        natural_language: str,
        schema_context: Dict[str, Any],
        connection_id: str
    ) -> Tuple[str, str, List[str]]:
        schema_description = self._build_schema_description(schema_context)
        
        system_prompt = """You are an expert Oracle SQL query generator. Your task is to convert natural language questions into accurate Oracle SQL queries.

Rules:
1. Always use proper Oracle SQL syntax
2. Use double quotes for identifiers (table names, column names) that contain special characters or are case-sensitive
3. For string literals, use single quotes
4. Use ROWNUM or FETCH FIRST N ROWS ONLY for limiting results
5. Always consider performance and use proper JOIN syntax (ANSI joins preferred)

Return your response in this exact JSON format:
{
    "sql": "the generated SQL query",
    "explanation": "brief explanation of what the query does",
    "tables_used": ["list of table names used"]
}
"""
        
        user_prompt = f"""Natural Language Question: {natural_language}

Schema Context:
{schema_description}

Generate the Oracle SQL query for the above question."""

        if self.llm_provider == "openai" and self.openai_client:
            return self._generate_with_openai(system_prompt, user_prompt, schema_context)
        elif self.llm_provider == "anthropic" and self.anthropic_client:
            return self._generate_with_anthropic(system_prompt, user_prompt, schema_context)
        else:
            return "", "LLM provider not configured or API key missing", []
    
    def _generate_with_openai(
        self, 
        system_prompt: str, 
        user_prompt: str,
        schema_context: Dict[str, Any]
    ) -> Tuple[str, str, List[str]]:
        try:
            response = self.openai_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            return self._parse_sql_response(content, schema_context)
        except Exception as e:
            return "", f"OpenAI API error: {str(e)}", []
    
    def _generate_with_anthropic(
        self, 
        system_prompt: str, 
        user_prompt: str,
        schema_context: Dict[str, Any]
    ) -> Tuple[str, str, List[str]]:
        try:
            response = self.anthropic_client.messages.create(
                model=self.llm_model,
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            content = response.content[0].text
            return self._parse_sql_response(content, schema_context)
        except Exception as e:
            return "", f"Anthropic API error: {str(e)}", []
    
    def _parse_sql_response(
        self, 
        content: str, 
        schema_context: Dict[str, Any]
    ) -> Tuple[str, str, List[str]]:
        import json
        try:
            data = json.loads(content)
            sql = data.get("sql", "")
            explanation = data.get("explanation", "")
            tables_used = data.get("tables_used", [])
            return sql, explanation, tables_used
        except json.JSONDecodeError:
            import re
            sql_match = re.search(r'```sql\s*(.*?)\s*```', content, re.DOTALL)
            if sql_match:
                sql = sql_match.group(1).strip()
            else:
                sql = content.strip()
            return sql, "Generated SQL query", []
    
    def _build_schema_description(self, schema_context: Dict[str, Any]) -> str:
        description_parts = []
        
        if "tables" in schema_context:
            for table in schema_context["tables"]:
                cols = []
                for col in table.get("columns", []):
                    col_desc = f"  - {col['name']}: {col['data_type']}"
                    if not col.get("nullable", True):
                        col_desc += " NOT NULL"
                    if col.get("default_value"):
                        col_desc += f" DEFAULT {col['default_value']}"
                    cols.append(col_desc)
                
                pks = table.get("primary_keys", [])
                if pks:
                    cols.append(f"  PRIMARY KEY: {', '.join(pks)}")
                
                fks = table.get("foreign_keys", [])
                for fk in fks:
                    cols.append(f"  FOREIGN KEY -> {fk['referenced_table']}({', '.join(fk['referenced_columns'])})")
                
                table_str = f"Table: {table['name']}\n" + "\n".join(cols)
                description_parts.append(table_str)
        
        return "\n\n".join(description_parts)
    
    def explain_query(self, sql: str, schema_context: Dict[str, Any]) -> str:
        system_prompt = """You are an expert at explaining SQL queries. Provide a clear, concise explanation of what the SQL query does in natural language."""
        
        user_prompt = f"SQL Query:\n{sql}\n\nExplain what this query does."
        
        if self.openai_client:
            try:
                response = self.openai_client.chat.completions.create(
                    model=self.llm_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.1,
                    max_tokens=500
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"Error explaining query: {str(e)}"
        
        return "LLM provider not configured"


class EmbeddingService:
    def __init__(self):
        self.model_name = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION
        self._model = None
    
    def _get_model(self):
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except Exception:
                pass
        return self._model
    
    def get_openai_embedding(self, text: str) -> List[float]:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def get_embedding(self, text: str) -> List[float]:
        try:
            return self.get_openai_embedding(text)
        except Exception:
            pass
        
        model = self._get_model()
        if model:
            embedding = model.encode(text)
            return embedding.tolist()
        
        return [0.0] * self.dimension
    
    def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        try:
            return self.get_openai_embeddings_batch(texts)
        except Exception:
            pass
        
        model = self._get_model()
        if model:
            embeddings = model.encode(texts)
            return embeddings.tolist()
        
        return [[0.0] * self.dimension for _ in texts]
    
    def get_openai_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        return [item.embedding for item in response.data]
    
    def text_to_vector_record(
        self,
        row_data: Dict[str, Any],
        columns: List[str],
        text_columns: List[str] = None
    ) -> str:
        if text_columns is None:
            text_columns = [c for c in columns if isinstance(row_data.get(c), str)]
        
        parts = []
        for col in text_columns:
            if col in row_data and row_data[col] is not None:
                parts.append(f"{col}: {str(row_data[col])}")
        
        for col in columns:
            if col not in text_columns and col in row_data and row_data[col] is not None:
                parts.append(f"{col}: {str(row_data[col])}")
        
        return "; ".join(parts)
