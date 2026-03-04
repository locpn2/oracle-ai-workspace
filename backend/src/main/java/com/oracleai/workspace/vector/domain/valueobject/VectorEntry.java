package com.oracleai.workspace.vector.domain.valueobject;

public record VectorEntry(
    RowId rowId,
    String document,
    float[] embedding,
    double similarityScore
) {
    public VectorEntry {
        if (embedding != null && embedding.length != 768) {
            throw new IllegalArgumentException("Embedding must have exactly 768 dimensions");
        }
        if (document == null || document.isBlank()) {
            throw new IllegalArgumentException("Document cannot be null or blank");
        }
    }

    public boolean hasValidEmbedding() {
        return embedding != null && embedding.length == 768;
    }

    public record RowId(String value) {
        public RowId {
            if (value == null || value.isBlank()) {
                throw new IllegalArgumentException("Row ID cannot be null or blank");
            }
        }
    }
}
