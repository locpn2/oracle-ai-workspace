import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from app.models.schemas import (
    ConnectionCreate, ConnectionUpdate, ConnectionResponse,
    AIQueryRequest, VectorCollectionCreate
)


def test_connection_create_validation():
    conn = ConnectionCreate(
        name="Test DB",
        host="localhost",
        port=1521,
        username="system",
        password="password",
        service_name="ORCL"
    )
    
    assert conn.name == "Test DB"
    assert conn.host == "localhost"
    assert conn.port == 1521


def test_connection_create_defaults():
    conn = ConnectionCreate(
        name="Test DB",
        host="localhost",
        username="system",
        password="password"
    )
    
    assert conn.port == 1521


def test_ai_query_request():
    request = AIQueryRequest(
        connection_id="test-id",
        natural_language="Show all customers"
    )
    
    assert request.connection_id == "test-id"
    assert request.natural_language == "Show all customers"
    assert request.max_rows == 100


def test_vector_collection_create():
    collection = VectorCollectionCreate(
        name="customer_vectors",
        connection_id="conn-id",
        source_schema="SALES",
        source_table="CUSTOMERS",
        text_columns=["NAME", "EMAIL"]
    )
    
    assert collection.name == "customer_vectors"
    assert collection.source_table == "CUSTOMERS"
    assert "NAME" in collection.text_columns
