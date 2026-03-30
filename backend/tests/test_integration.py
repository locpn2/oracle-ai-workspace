import pytest
import pytest_asyncio
from unittest.mock import patch, AsyncMock, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestAuthIntegration:
    """Test authentication endpoints"""

    def test_login_success(self):
        """Test successful login"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "demo@oraclevision.com", "password": "demo123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == "demo@oraclevision.com"

    def test_login_invalid_password(self):
        """Test login with invalid password"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "demo@oraclevision.com", "password": "wrongpassword"}
        )
        assert response.status_code == 401

    def test_login_invalid_email(self):
        """Test login with invalid email"""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "nonexistent@test.com", "password": "anypassword"}
        )
        assert response.status_code == 401

    def test_register_new_user(self):
        """Test user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "newuser@test.com", "name": "New User", "password": "password123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@test.com"
        assert data["name"] == "New User"

    def test_register_duplicate_email(self):
        """Test registration with duplicate email"""
        client.post(
            "/api/v1/auth/register",
            json={"email": "duplicate@test.com", "name": "User One", "password": "password123"}
        )
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "duplicate@test.com", "name": "User Two", "password": "password456"}
        )
        assert response.status_code == 400


class TestQueryIntegration:
    """Test query endpoints"""

    def test_text_to_sql_endpoint(self):
        """Test text-to-sql endpoint returns SQL or fallback error"""
        response = client.post(
            "/api/v1/query/text-to-sql",
            json={"natural_language": "show customers"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "sql" in data
        assert "confidence" in data

    def test_text_to_sql_with_context(self):
        """Test text-to-sql with context"""
        response = client.post(
            "/api/v1/query/text-to-sql",
            json={
                "natural_language": "count orders",
                "context": "Tables: ORDERS(order_id, customer_id, order_date)"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "sql" in data

    def test_text_to_sql_stream_endpoint(self):
        """Test SSE streaming endpoint"""
        response = client.post(
            "/api/v1/query/text-to-sql/stream",
            json={"natural_language": "show customers"}
        )
        assert response.status_code == 200
        assert "text/event-stream" in response.headers.get("content-type", "")

    def test_execute_query(self):
        """Test query execution"""
        response = client.post(
            "/api/v1/query/execute",
            json={"sql": "SELECT * FROM customers WHERE ROWNUM <= 5", "page": 1, "page_size": 10}
        )
        assert response.status_code == 200
        data = response.json()
        assert "columns" in data
        assert "rows" in data

    def test_execute_invalid_sql(self):
        """Test execution with invalid SQL"""
        response = client.post(
            "/api/v1/query/execute",
            json={"sql": "SELECT * FROM nonexistent_table", "page": 1, "page_size": 10}
        )
        assert response.status_code == 200

    def test_query_history(self):
        """Test query history endpoint"""
        client.post(
            "/api/v1/query/text-to-sql",
            json={"natural_language": "test query"}
        )
        response = client.get("/api/v1/query/history?limit=10")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_query_preview(self):
        """Test SQL preview/validation"""
        response = client.post(
            "/api/v1/query/preview",
            data="SELECT * FROM customers"
        )
        assert response.status_code == 200

    def test_explain_query(self):
        """Test execution plan"""
        response = client.post(
            "/api/v1/query/explain",
            json={"sql": "SELECT * FROM customers WHERE customer_id = 1"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "sql" in data


class TestSchemaIntegration:
    """Test schema endpoints"""

    def test_get_tables(self):
        """Test get all tables"""
        response = client.get("/api/v1/schema/tables")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_table_details(self):
        """Test get table details"""
        response = client.get("/api/v1/schema/tables/CUSTOMERS")
        assert response.status_code == 200

    def test_get_erd(self):
        """Test ERD generation"""
        response = client.get("/api/v1/schema/erd")
        assert response.status_code == 200
        data = response.json()
        assert "nodes" in data
        assert "edges" in data


class TestVectorIntegration:
    """Test vector endpoints"""

    def test_vector_status(self):
        """Test vector sync status"""
        response = client.get("/api/v1/vector/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    def test_vector_search(self):
        """Test semantic search"""
        response = client.post(
            "/api/v1/vector/search",
            json={"query": "customer orders", "top_k": 3}
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data

    def test_vector_clear(self):
        """Test clear embeddings"""
        response = client.delete("/api/v1/vector/clear")
        assert response.status_code == 200

    def test_vector_models(self):
        """Test list Ollama models"""
        response = client.get("/api/v1/vector/models")
        assert response.status_code == 200
        data = response.json()
        assert "available" in data


class TestHealthEndpoint:
    """Test health check"""

    def test_health_check(self):
        """Test health endpoint"""
        response = client.get("/health")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
