package com.oracleai.workspace.vector.domain.valueobject;

public record RowId(String value) {
    public RowId {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("RowId cannot be blank");
        }
    }
}
