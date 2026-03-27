import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    from unittest.mock import MagicMock
    settings = MagicMock()
    settings.oracle_host = "localhost"
    settings.oracle_port = 1521
    settings.oracle_service = "XEPDB1"
    settings.oracle_user = "test"
    settings.oracle_password = "test"
    settings.postgres_host = "localhost"
    settings.postgres_port = 5432
    settings.postgres_db = "test"
    settings.postgres_user = "test"
    settings.postgres_password = "test"
    settings.secret_key = "test-secret-key"
    settings.algorithm = "HS256"
    settings.access_token_expire_minutes = 30
    settings.default_llm_provider = "ollama"
    settings.ollama_base_url = "http://localhost:11434"
    settings.ollama_model = "llama3.2"
    settings.ollama_embed_model = "nomic-embed-text"
    return settings


@pytest.fixture
def mock_oracle_tables():
    """Mock Oracle tables for testing"""
    return [
        {"name": "CUSTOMERS", "schema": "ORACLEVISION"},
        {"name": "ORDERS", "schema": "ORACLEVISION"},
        {"name": "PRODUCTS", "schema": "ORACLEVISION"},
    ]


@pytest.fixture
def sample_query_request():
    """Sample query request"""
    return {
        "natural_language": "show me all customers",
        "context": None
    }