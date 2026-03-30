import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.text_to_sql import (
    convert_text_to_sql,
    generate_fallback_response,
    generate_template_sql,
    extract_tables,
    get_schema_context,
    is_ollama_available,
    classify_query_complexity if False else None,
)
from app.llm.router import classify_query_complexity


class TestExtractTables:

    def test_extract_tables_with_join(self):
        sql = "SELECT * FROM customers JOIN orders ON customers.id = orders.customer_id"
        tables = extract_tables(sql)
        assert "customers" in tables
        assert "orders" in tables

    def test_extract_tables_single(self):
        sql = "SELECT * FROM products"
        tables = extract_tables(sql)
        assert "products" in tables


class TestTemplateFallback:

    def test_show_customers(self):
        result = generate_template_sql("show customers")
        assert result is not None
        assert "CUSTOMERS" in result["sql"]
        assert result["llm_used"] is False
        assert result["confidence"] > 0

    def test_list_orders(self):
        result = generate_template_sql("list all orders")
        assert result is not None
        assert "ORDERS" in result["sql"]

    def test_count_orders(self):
        result = generate_template_sql("count orders")
        assert result is not None
        assert "COUNT" in result["sql"].upper()
        assert "ORDERS" in result["sql"].upper()

    def test_top_n_products(self):
        result = generate_template_sql("top 5 products")
        assert result is not None
        assert "PRODUCTS" in result["sql"]
        assert "ROWNUM" in result["sql"]

    def test_max_salary(self):
        result = generate_template_sql("max salary in employees")
        assert result is not None
        assert "MAX" in result["sql"].upper()

    def test_avg_salary(self):
        result = generate_template_sql("average salary")
        assert result is not None
        assert "AVG" in result["sql"].upper()

    def test_unmatched_query_returns_none(self):
        result = generate_template_sql("something completely random xyz123")
        assert result is None


class TestFallbackResponse:

    def test_template_match_returns_sql(self):
        result = generate_fallback_response("show customers")
        assert result["sql"] != ""
        assert result["llm_used"] is False

    def test_no_match_returns_error(self):
        result = generate_fallback_response("complex impossible query xyz")
        assert result["sql"] == ""
        assert result["confidence"] == 0
        assert "error" in result
        assert "LLM" in result["error"]


class TestQueryClassification:

    def test_simple_show(self):
        assert classify_query_complexity("show customers") == "simple"

    def test_simple_count(self):
        assert classify_query_complexity("count orders") == "simple"

    def test_simple_list(self):
        assert classify_query_complexity("list all products") == "simple"

    def test_complex_join(self):
        assert classify_query_complexity("find customers with most orders last month") == "complex"

    def test_complex_subquery(self):
        assert classify_query_complexity("employees who earn more than average") == "complex"


class TestConvertTextToSQL:

    @pytest.mark.asyncio
    @patch('app.services.text_to_sql.ollama_client')
    async def test_ollama_unavailable_falls_back(self, mock_ollama):
        mock_ollama.is_available = AsyncMock(return_value=False)

        result = await convert_text_to_sql("show customers", use_vector=False)

        assert result["llm_used"] is False
        assert "CUSTOMERS" in result["sql"]

    @pytest.mark.asyncio
    @patch('app.services.text_to_sql.ollama_client')
    async def test_ollama_unavailable_complex_query_fails_clearly(self, mock_ollama):
        mock_ollama.is_available = AsyncMock(return_value=False)

        result = await convert_text_to_sql(
            "find correlation between employee salary and order volume",
            use_vector=False
        )

        assert result["sql"] == ""
        assert result["confidence"] == 0
        assert "error" in result

    @pytest.mark.asyncio
    async def test_schema_context(self):
        context = await get_schema_context(use_vector=False)
        assert "CUSTOMERS" in context
        assert "ORDERS" in context


class TestMockData:

    def test_mock_tables_exist(self):
        from app.db.oracle import MOCK_TABLES
        assert len(MOCK_TABLES) > 0
        assert any(t["name"] == "CUSTOMERS" for t in MOCK_TABLES)

    def test_mock_columns_exist(self):
        from app.db.oracle import MOCK_COLUMNS
        assert "CUSTOMERS" in MOCK_COLUMNS
        assert len(MOCK_COLUMNS["CUSTOMERS"]) > 0


class TestSecurity:

    def test_password_hashing(self):
        from app.core.security import get_password_hash, verify_password

        password = "testpassword123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_token_creation(self):
        from app.core.security import create_access_token, verify_token
        from datetime import timedelta

        token = create_access_token(
            data={"sub": "user123", "email": "test@example.com"},
            expires_delta=timedelta(minutes=30)
        )

        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "user123"
        assert payload["email"] == "test@example.com"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
