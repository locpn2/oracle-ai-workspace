import pytest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from app.services.ai_service import AIService, EmbeddingService


def test_ai_service_initialization():
    service = AIService()
    assert service.llm_provider in ["openai", "anthropic"]


def test_build_schema_description():
    service = AIService()
    
    schema_context = {
        "tables": [
            {
                "name": "EMPLOYEES",
                "columns": [
                    {"name": "ID", "data_type": "NUMBER", "nullable": False},
                    {"name": "NAME", "data_type": "VARCHAR2", "nullable": True}
                ],
                "primary_keys": ["ID"],
                "foreign_keys": []
            }
        ]
    }
    
    description = service._build_schema_description(schema_context)
    
    assert "EMPLOYEES" in description
    assert "ID" in description
    assert "NUMBER" in description


def test_text_to_vector_record():
    service = EmbeddingService()
    
    row_data = {
        "ID": 1,
        "NAME": "John Doe",
        "DEPARTMENT": "IT"
    }
    columns = ["ID", "NAME", "DEPARTMENT"]
    
    result = service.text_to_vector_record(row_data, columns)
    
    assert "ID: 1" in result
    assert "NAME: John Doe" in result


def test_embedding_service_dimension():
    service = EmbeddingService()
    assert service.dimension == 384
