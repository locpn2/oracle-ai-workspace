from typing import Optional, List
import re
import asyncio
from ..core.config import get_settings
from ..llm.router import llm_provider
from ..llm.ollama import ollama_client
from ..services.vector import vector_service
from ..llm.prompts.text_to_sql import SYSTEM_PROMPT, USER_PROMPT

settings = get_settings()

MOCK_SCHEMA = """
Schema Information:
- CUSTOMERS: customer_id (PK), name, email, phone, address, created_at
- ORDERS: order_id (PK), customer_id (FK), order_date, total_amount, status
- PRODUCTS: product_id (PK), name, category, price, stock_quantity
- ORDER_ITEMS: item_id (PK), order_id (FK), product_id (FK), quantity, price
- EMPLOYEES: employee_id (PK), name, department, salary, hire_date
"""

FALLBACK_TEMPLATES = {
    "show": "SELECT",
    "list": "SELECT",
    "get": "SELECT",
    "find": "SELECT",
    "total": "SUM",
    "count": "COUNT",
    "average": "AVG",
    "max": "MAX",
    "min": "MIN",
    "top": "ROWNUM <= 10",
    "customers": "CUSTOMERS",
    "orders": "ORDERS",
    "products": "PRODUCTS",
    "employees": "EMPLOYEES",
}

KNOWN_TABLES = ["CUSTOMERS", "ORDERS", "PRODUCTS", "ORDER_ITEMS", "EMPLOYEES"]


async def get_schema_context(use_vector: bool = False) -> str:
    """Get schema context, optionally from vector DB"""
    if use_vector:
        try:
            context = vector_service.get_schema_context()
            if context:
                return context
        except Exception as e:
            print(f"Error getting vector schema context: {e}")
    return MOCK_SCHEMA


async def is_ollama_available() -> bool:
    """Check if Ollama is available"""
    try:
        return await ollama_client.is_available()
    except:
        return False


def extract_tables(sql: str) -> List[str]:
    """Extract table names from SQL"""
    pattern = r'FROM\s+(\w+)|JOIN\s+(\w+)'
    matches = re.findall(pattern, sql, re.IGNORECASE)
    return [m[0] or m[1] for m in matches if m[0] or m[1]]


def generate_fallback_sql(natural_language: str) -> dict:
    """Generate SQL using template-based fallback (when LLM unavailable)"""
    nl_lower = natural_language.lower()
    
    sql_parts = ["SELECT * FROM "]
    table_found = False
    
    for keyword, replacement in FALLBACK_TEMPLATES.items():
        if keyword in nl_lower:
            if keyword.upper() in KNOWN_TABLES:
                sql_parts = ["SELECT * FROM ", replacement]
                table_found = True
                break
    
    if not table_found:
        sql_parts = ["SELECT * FROM CUSTOMERS"]
    
    if "total" in nl_lower or "count" in nl_lower:
        for table in KNOWN_TABLES:
            if table.lower() in nl_lower:
                sql_parts = [f"SELECT COUNT(*) as total FROM {table}"]
                break
        else:
            sql_parts = ["SELECT COUNT(*) as total FROM CUSTOMERS"]
    
    if "top" in nl_lower or "limit" in nl_lower:
        sql_parts.append(" WHERE ROWNUM <= 10")
    
    if "where" in nl_lower or "filter" in nl_lower:
        sql_parts.append(" WHERE ROWNUM <= 10")
    
    sql = " ".join(sql_parts)
    
    if nl_lower.startswith(("show", "list", "get", "find")):
        for table in KNOWN_TABLES:
            if table.lower() in nl_lower:
                sql = f"SELECT * FROM {table} WHERE ROWNUM <= 10"
                break
    
    return {
        "sql": sql,
        "confidence": 0.5,
        "explanation": "Generated using template-based fallback (LLM unavailable)",
        "llm_used": False
    }


async def convert_text_to_sql(natural_language: str, context: Optional[str] = None, 
                              use_vector: bool = True) -> dict:
    """Convert natural language to SQL using LLM or fallback"""
    
    ollama_available = await is_ollama_available()
    
    if not ollama_available:
        return generate_fallback_sql(natural_language)
    
    try:
        schema_context = context
        if not schema_context and use_vector:
            try:
                semantic_results = await vector_service.semantic_search(natural_language, top_k=3)
                if semantic_results:
                    table_names = list(set([r.get("table_name") for r in semantic_results]))
                    schema_context = vector_service.get_schema_context(table_names)
            except Exception as e:
                print(f"Error in semantic search: {e}")
        
        if not schema_context:
            schema_context = await get_schema_context(use_vector)
        
        system_prompt = SYSTEM_PROMPT.format(schema_context=schema_context)
        user_prompt = USER_PROMPT.format(
            schema_context=schema_context,
            query=natural_language
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        result = await llm_provider.chat(messages, temperature=0.3)
        
        sql = result.strip()
        
        sql = re.sub(r'^```sql\n', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'^```\n', '', sql)
        sql = re.sub(r'\n```$', '', sql)
        
        return {
            "sql": sql,
            "confidence": 0.85,
            "explanation": "Generated using Ollama LLM",
            "llm_used": True,
            "model": settings.default_llm_provider
        }
        
    except Exception as e:
        print(f"Error in text-to-sql conversion: {e}")
        return generate_fallback_sql(natural_language)


text_to_sql_service = type('TextToSQLService', (), {
    'convert': lambda self, nl, ctx=None, use_vector=True: convert_text_to_sql(nl, ctx, use_vector)
})()
