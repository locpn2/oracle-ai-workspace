from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "OracleVision"
    debug: bool = False
    
    # Oracle
    oracle_host: str = "localhost"
    oracle_port: int = 1521
    oracle_service: str = "XEPDB1"
    oracle_user: str = "system"
    oracle_password: str = ""
    
    # PostgreSQL (pgvector)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "oracle_vision"
    postgres_user: str = "postgres"
    postgres_password: str = ""
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # JWT
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # LLM Providers
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"
    default_llm_provider: str = "openai"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
