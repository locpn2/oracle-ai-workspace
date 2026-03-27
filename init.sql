-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create schema table for vector storage
CREATE TABLE IF NOT EXISTS schema_embeddings (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(255) NOT NULL,
    column_name VARCHAR(255),
    description TEXT,
    embedding vector(1536),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for vector search
CREATE INDEX IF NOT EXISTS idx_schema_embeddings ON schema_embeddings USING ivfflat (embedding vector_cosine_ops);

-- Create query history table
CREATE TABLE IF NOT EXISTS query_history (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    natural_language TEXT NOT NULL,
    generated_sql TEXT NOT NULL,
    success BOOLEAN DEFAULT true,
    execution_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create schema groups table
CREATE TABLE IF NOT EXISTS schema_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    color VARCHAR(50),
    user_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create group memberships table
CREATE TABLE IF NOT EXISTS group_tables (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES schema_groups(id) ON DELETE CASCADE,
    table_name VARCHAR(255) NOT NULL
);
