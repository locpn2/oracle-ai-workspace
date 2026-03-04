package com.oracleai.workspace.vector.domain.valueobject;

public enum EmbeddingModel {
    BGE_BASE("bge-base"),
    SQLCODER_7B("sqlcoder-7b"),
    NOMIC_EMBED("nomic-embed-text");

    private final String modelName;

    EmbeddingModel(String modelName) {
        this.modelName = modelName;
    }

    public String getModelName() {
        return modelName;
    }
}
