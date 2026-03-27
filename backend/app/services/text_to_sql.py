from typing import Optional
import re
from ..core.config import get_settings

settings = get_settings()


async def get_schema_context() -> str:
    return """
    Schema Information:
    - CUSTOMERS: customer_id (PK), name, email, phone, address, created_at
    - ORDERS: order_id (PK), customer_id (FK), order_date, total_amount, status
    - PRODUCTS: product_id (PK), name, category, price, stock_quantity
    - ORDER_ITEMS: item_id (PK), order_id (FK), product_id (FK), quantity, price
    - EMPLOYEES: employee_id (PK), name, department, salary, hire_date
    """


def extract_tables(sql: str) -> list[str]:
    pattern = r'FROM\s+(\w+)|JOIN\s+(\w+)'
    matches = re.findall(pattern, sql, re.IGNORECASE)
    return [m[0] or m[1] for m in matches if m[0] or m[1]]


async def convert_text_to_sql(natural_language: str, context: Optional[str] = None) -> dict:
    schema_context = context or await get_schema_context()
    
    prompt = f"""Convert this natural language query to Oracle SQL.

Schema:
{schema_context}

Query: {natural_language}

Rules:
- Use Oracle SQL syntax
- Use ROWNUM for pagination, not LIMIT
- Use SYSDATE for current date
- Return only the SQL, no explanation

SQL:"""

    templates = {
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
    }
    
    sql_parts = ["SELECT * FROM "]
    table_found = False
    
    for keyword, replacement in templates.items():
        if keyword.lower() in natural_language.lower():
            if keyword.upper() in ["CUSTOMERS", "ORDERS", "PRODUCTS", "EMPLOYEES"]:
                sql_parts = ["SELECT * FROM ", replacement]
                table_found = True
                break
    
    if not table_found:
        sql_parts = ["SELECT * FROM CUSTOMERS"]
    
    if "total" in natural_language.lower():
        sql_parts = [f"SELECT COUNT(*) as total FROM CUSTOMERS"]
    
    if "top" in natural_language.lower() or "limit" in natural_language.lower():
        sql_parts.append(" WHERE ROWNUM <= 10")
    
    sql = " ".join(sql_parts)
    
    if natural_language.lower().startswith(("show", "list", "get", "find")):
        for table in ["CUSTOMERS", "ORDERS", "PRODUCTS", "EMPLOYEES"]:
            if table.lower() in natural_language.lower():
                sql = f"SELECT * FROM {table} WHERE ROWNUM <= 10"
                break
    
    return {
        "sql": sql,
        "confidence": 0.75,
        "explanation": "Generated SQL based on natural language query",
    }


text_to_sql_service = type('obj', (object,), {'convert': lambda self, nl, ctx=None: convert_text_to_sql(nl, ctx)})()
