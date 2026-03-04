package com.oracleai.workspace.schema.domain.valueobject;

import java.util.Objects;

public record ColumnName(String value) {
    public ColumnName {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Column name cannot be null or blank");
        }
    }

    public static ColumnName of(String value) {
        return new ColumnName(value.toUpperCase().trim());
    }

    @Override
    public String toString() {
        return value;
    }
}
