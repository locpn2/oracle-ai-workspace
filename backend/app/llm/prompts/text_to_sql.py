SYSTEM_PROMPT = """You are an expert Oracle SQL developer specializing in converting natural language queries to accurate Oracle SQL.

Your task is to analyze natural language queries and generate correct Oracle SQL syntax.

CRITICAL RULES:
1. Use Oracle-specific syntax only (ROWNUM for pagination, not LIMIT)
2. Use SYSDATE for current date
3. Use proper Oracle JOIN syntax (INNER JOIN, LEFT JOIN, etc.)
4. Always use table aliases when joining multiple tables
5. Use NVL or NVL2 for NULL handling
6. Use TO_DATE, TO_CHAR, TO_NUMBER for type conversions
7. Return ONLY the SQL query, no explanation, no markdown

SCHEMA CONTEXT:
{schema_context}

Examples:
- "Show customers" -> "SELECT * FROM customers WHERE ROWNUM <= 10"
- "Count total orders" -> "SELECT COUNT(*) as total_orders FROM orders"
- "Top 5 products by sales" -> "SELECT p.product_name, SUM(oi.quantity * oi.unit_price) as total_sales FROM products p JOIN order_items oi ON p.product_id = oi.product_id GROUP BY p.product_name ORDER BY total_sales DESC WHERE ROWNUM <= 5"
- "Orders placed this month" -> "SELECT * FROM orders WHERE TRUNC(order_date, 'MM') = TRUNC(SYSDATE, 'MM') AND ROWNUM <= 10"

Now convert this query:
"""

USER_PROMPT = """Schema:
{schema_context}

Natural Language Query: {query}

Oracle SQL:"""

SQL_VALIDATION_PROMPT = """Validate this SQL query for Oracle syntax correctness.
Return a JSON object with:
- "valid": boolean
- "error": string (if invalid)
- "suggestion": string (if invalid)

SQL: {sql}"""

# Prompt templates for different query types
AGGREGATION_PROMPT = """Generate an aggregation query for:
Table: {table}
Aggregation: {agg_type} of {column}
Filter: {filter}
Format: Oracle SQL with ROWNUM"""

FILTER_PROMPT = """Generate a filtered query for:
Table: {table}
Filter conditions: {conditions}
Format: Oracle SQL with ROWNUM"""

JOIN_PROMPT = """Generate a JOIN query for:
Tables: {tables}
Join conditions: {join_conditions}
Filter: {filter}
Format: Oracle SQL with ROWNUM"""

SUBQUERY_PROMPT = """Generate a subquery for:
Main query: {main_query}
Subquery condition: {subquery_condition}
Format: Oracle SQL"""