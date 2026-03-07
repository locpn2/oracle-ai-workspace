package com.oracleai.workspace.schema.domain.valueobject;

public record ConstraintName(String value) {
    public ConstraintName {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("ConstraintName cannot be blank");
        }
    }
}
