from typing import Optional, List
import re
import asyncio
from ..core.config import get_settings
from ..llm.router import llm_provider
from ..llm.ollama import ollama_client
from ..services.vector import vector_service
from ..llm.prompts.text_to_sql import SYSTEM_PROMPT, USER_PROMPT, SQL_VALIDATION_PROMPT

settings = get_settings()

MOCK_SCHEMA = """
Schema Information:
- CUSTOMERS: customer_id (PK), name, email, phone, address, created_at
- ORDERS: order_id (PK), customer_id (FK), order_date, total_amount, status
- PRODUCTS: product_id (PK), name, category, price, stock_quantity
- ORDER_ITEMS: item_id (PK), order_id (FK), product_id (FK), quantity, price
- EMPLOYEES: employee_id (PK), name, department, salary, hire_date
"""

KNOWN_TABLES = ["CUSTOMERS", "ORDERS", "PRODUCTS", "ORDER_ITEMS", "EMPLOYEES"]

# Table columns for template matching
TABLE_COLUMNS = {
    "CUSTOMERS": ["customer_id", "name", "email", "phone", "address", "created_at"],
    "ORDERS": ["order_id", "customer_id", "order_date", "total_amount", "status"],
    "PRODUCTS": ["product_id", "name", "category", "price", "stock_quantity"],
    "ORDER_ITEMS": ["item_id", "order_id", "product_id", "quantity", "price"],
    "EMPLOYEES": ["employee_id", "name", "department", "salary", "hire_date"],
}

# SQL templates for common patterns (used when LLM unavailable)
SQL_TEMPLATES = [
    {
        "name": "show_table",
        "pattern": r"(?:show|list|get|find|display)\s+(?:all\s+)?(\w+)",
        "build": lambda m: _build_show_table(m.group(1)),
    },
    {
        "name": "count_table",
        "pattern": r"(?:count|total|how many)\s+(?:all\s+)?(\w+)",
        "build": lambda m: _build_count(m.group(1)),
    },
    {
        "name": "top_n",
        "pattern": r"top\s+(\d+)\s+(\w+)",
        "build": lambda m: _build_top_n(m.group(2), m.group(1)),
    },
    {
        "name": "max_column",
        "pattern": r"(?:max|highest|most)\s+(\w+)\s+(?:in|from|of)\s+(\w+)",
        "build": lambda m: _build_aggregate(m.group(2), m.group(1), "MAX"),
    },
    {
        "name": "min_column",
        "pattern": r"(?:min|lowest|least)\s+(\w+)\s+(?:in|from|of)\s+(\w+)",
        "build": lambda m: _build_aggregate(m.group(2), m.group(1), "MIN"),
    },
    {
        "name": "avg_column",
        "pattern": r"(?:average|avg|mean)\s+(\w+)",
        "build": lambda m: _build_avg(m.group(1)),
    },
]


def _find_table(name: str) -> Optional[str]:
    """Find matching table name (case-insensitive)"""
    name_lower = name.lower().rstrip("s")  # remove plural
    for table in KNOWN_TABLES:
        if table.lower() == name_lower or table.lower().rstrip("s") == name_lower:
            return table
    return None


def _find_column(table: str, col_name: str) -> Optional[str]:
    """Find matching column in table"""
    if table not in TABLE_COLUMNS:
        return None
    col_lower = col_name.lower()
    for col in TABLE_COLUMNS[table]:
        if col.lower() == col_lower:
            return col
    return None


def _build_show_table(table_name: str) -> Optional[dict]:
    table = _find_table(table_name)
    if not table:
        return None
    return {
        "sql": f"SELECT * FROM {table} WHERE ROWNUM <= 10",
        "confidence": 0.7,
        "explanation": f"Show first 10 rows from {table}",
    }


def _build_count(table_name: str) -> Optional[dict]:
    table = _find_table(table_name)
    if not table:
        return None
    return {
        "sql": f"SELECT COUNT(*) as total FROM {table}",
        "confidence": 0.7,
        "explanation": f"Count all rows in {table}",
    }


def _build_top_n(table_name: str, n: str) -> Optional[dict]:
    table = _find_table(table_name)
    if not table:
        return None
    numeric_cols = [c for c in TABLE_COLUMNS.get(table, []) if any(
        k in c.lower() for k in ["price", "amount", "salary", "quantity", "total"]
    )]
    order_col = numeric_cols[0] if numeric_cols else TABLE_COLUMNS[table][0]
    return {
        "sql": f"SELECT * FROM {table} WHERE ROWNUM <= {n} ORDER BY {order_col} DESC",
        "confidence": 0.65,
        "explanation": f"Top {n} from {table} ordered by {order_col}",
    }


def _build_aggregate(table_name: str, col_name: str, func: str) -> Optional[dict]:
    table = _find_table(table_name)
    if not table:
        return None
    col = _find_column(table, col_name) or col_name
    return {
        "sql": f"SELECT {func}({col}) as result FROM {table}",
        "confidence": 0.65,
        "explanation": f"{func} of {col} in {table}",
    }


def _build_avg(col_name: str) -> Optional[dict]:
    col_lower = col_name.lower()
    for table, cols in TABLE_COLUMNS.items():
        for col in cols:
            if col_lower in col.lower():
                return {
                    "sql": f"SELECT AVG({col}) as average_{col} FROM {table}",
                    "confidence": 0.65,
                    "explanation": f"Average {col} from {table}",
                }
    return None


def generate_template_sql(natural_language: str) -> Optional[dict]:
    """Try to generate SQL using predefined templates. Returns None if no match."""
    nl_lower = natural_language.lower().strip()

    for template in SQL_TEMPLATES:
        match = re.search(template["pattern"], nl_lower)
        if match:
            result = template["build"](match)
            if result:
                result["llm_used"] = False
                return result

    return None


def generate_fallback_response(natural_language: str) -> dict:
    """Generate fallback: try templates, fail clearly if no match"""
    template_result = generate_template_sql(natural_language)
    if template_result:
        return template_result

    return {
        "sql": "",
        "confidence": 0,
        "error": (
            "LLM service is unavailable and the query cannot be generated "
            "using templates. Please try simpler queries like 'show customers', "
            "'count orders', or 'top 5 products'."
        ),
        "llm_used": False,
    }


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
    except Exception:
        return False


def extract_tables(sql: str) -> List[str]:
    """Extract table names from SQL"""
    pattern = r'FROM\s+(\w+)|JOIN\s+(\w+)'
    matches = re.findall(pattern, sql, re.IGNORECASE)
    return [m[0] or m[1] for m in matches if m[0] or m[1]]


async def validate_sql(sql: str) -> dict:
    """Validate SQL syntax using LLM. Returns {valid: bool, error: str, suggestion: str}"""
    if not sql.strip():
        return {"valid": False, "error": "Empty SQL", "suggestion": None}

    try:
        validation_prompt = SQL_VALIDATION_PROMPT.format(sql=sql)
        messages = [
            {"role": "system", "content": "You are a SQL validator. Return only valid JSON."},
            {"role": "user", "content": validation_prompt}
        ]
        result = await llm_provider.chat(messages, temperature=0.1)
        if result:
            import json as _json
            cleaned = re.sub(r'^```json\n?', '', result.strip())
            cleaned = re.sub(r'\n?```$', '', cleaned)
            return _json.loads(cleaned)
    except Exception as e:
        print(f"SQL validation error: {e}")

    return {"valid": True, "error": None, "suggestion": None}


async def convert_text_to_sql(natural_language: str, context: Optional[str] = None,
                               use_vector: bool = True, validate: bool = True) -> dict:
    """Convert natural language to SQL using LLM with template fallback"""

    ollama_available = await is_ollama_available()

    if not ollama_available:
        return generate_fallback_response(natural_language)

    try:
        schema_context = context
        if not schema_context and use_vector:
            try:
                semantic_results = await vector_service.semantic_search(
                    natural_language, top_k=3
                )
                if semantic_results:
                    table_names = list(
                        set([r.get("table_name") for r in semantic_results])
                    )
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

        # Smart routing: pass query_hint for model selection
        result = await llm_provider.chat(
            messages, temperature=0.3, query_hint=natural_language
        )

        if not result:
            return generate_fallback_response(natural_language)

        sql = result.strip()
        sql = re.sub(r'^```sql\n?', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'^```\n?', '', sql)
        sql = re.sub(r'\n?```$', '', sql)
        sql = sql.strip()

        if not sql:
            return generate_fallback_response(natural_language)

        # Validate generated SQL
        validation_result = {"valid": True}
        if validate:
            validation_result = await validate_sql(sql)
            if not validation_result.get("valid", True):
                return {
                    "sql": sql,
                    "confidence": 0.4,
                    "explanation": f"Generated using LLM (validation warning: {validation_result.get('error', 'unknown')})",
                    "llm_used": True,
                    "validation_warning": validation_result.get("error"),
                    "suggestion": validation_result.get("suggestion"),
                }

        return {
            "sql": sql,
            "confidence": 0.85,
            "explanation": "Generated using LLM",
            "llm_used": True,
        }

    except Exception as e:
        print(f"Error in text-to-sql conversion: {e}")
        return generate_fallback_response(natural_language)


text_to_sql_service = type('TextToSQLService', (), {
    'convert': lambda self, nl, ctx=None, use_vector=True, validate=True: convert_text_to_sql(nl, ctx, use_vector, validate),
    'is_ollama_available': lambda self: is_ollama_available(),
    'generate_template_sql': staticmethod(generate_template_sql),
})()
