import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from app.config import Settings


def test_settings_defaults():
    settings = Settings()
    assert settings.APP_NAME == "OracleVision"
    assert settings.APP_VERSION == "1.0.0"
    assert settings.DEBUG is False
    assert settings.LLM_PROVIDER == "openai"


def test_settings_env_override(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("DEBUG", "true")
    
    settings = Settings()
    assert settings.OPENAI_API_KEY == "test-key"
    assert settings.DEBUG is True


def test_embedding_dimension():
    settings = Settings()
    assert settings.EMBEDDING_DIMENSION == 384
