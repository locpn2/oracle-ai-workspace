import pytest
from unittest.mock import patch, AsyncMock, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.text_to_sql import (
    convert_text_to_sql,
    generate_fallback_sql,
    extract_tables,
    get_schema_context,
    is_ollama_available,
)


class TestTextToSQL:
    
    def test_extract_tables(self):
        """Test SQL table extraction"""
        sql = "SELECT * FROM customers JOIN orders ON customers.id = orders.customer_id"
        tables = extract_tables(sql)
        assert "customers" in tables
        assert "orders" in tables
    
    def test_extract_tables_no_joins(self):
        """Test SQL table extraction without joins"""
        sql = "SELECT * FROM products"
        tables = extract_tables(sql)
        assert "products" in tables
    
    def test_generate_fallback_sql_show_customers(self):
        """Test fallback SQL generation for show customers"""
        result = generate_fallback_sql("show customers")
        assert "CUSTOMERS" in result["sql"]
        assert result["confidence"] == 0.5
        assert result["llm_used"] is False
    
    def test_generate_fallback_sql_count_orders(self):
        """Test fallback SQL generation for count"""
        result = generate_fallback_sql("count total orders")
        assert "COUNT" in result["sql"].upper()
        assert "ORDERS" in result["sql"].upper()
    
    def test_generate_fallback_sql_top_products(self):
        """Test fallback SQL generation for top N"""
        result = generate_fallback_sql("top 10 products")
        assert "PRODUCTS" in result["sql"]
        assert "ROWNUM" in result["sql"]
    
    @pytest.mark.asyncio
    @patch('app.services.text_to_sql.ollama_client')
    async def test_convert_text_to_sql_ollama_unavailable(self, mock_ollama):
        """Test text-to-sql when Ollama is not available"""
        mock_ollama.is_available = AsyncMock(return_value=False)
        
        result = await convert_text_to_sql("show customers", use_vector=False)
        
        assert "CUSTOMERS" in result["sql"]
        assert result["llm_used"] is False
    
    @pytest.mark.asyncio
    async def test_get_schema_context(self):
        """Test schema context retrieval"""
        context = await get_schema_context(use_vector=False)
        assert "CUSTOMERS" in context
        assert "ORDERS" in context


class TestMockData:
    """Test Oracle mock data"""
    
    def test_mock_tables_exist(self):
        """Test that mock tables are defined"""
        from app.db.oracle import MOCK_TABLES
        assert len(MOCK_TABLES) > 0
        assert any(t["name"] == "CUSTOMERS" for t in MOCK_TABLES)
    
    def test_mock_columns_exist(self):
        """Test that mock columns are defined"""
        from app.db.oracle import MOCK_COLUMNS
        assert "CUSTOMERS" in MOCK_COLUMNS
        assert len(MOCK_COLUMNS["CUSTOMERS"]) > 0


class TestSecurity:
    """Test security features"""
    
    def test_password_hashing(self):
        """Test password hashing"""
        from app.core.security import get_password_hash, verify_password
        
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False
    
    def test_token_creation(self):
        """Test JWT token creation"""
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