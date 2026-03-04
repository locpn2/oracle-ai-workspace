package com.oracleai.workspace.schema.domain.valueobject;

import java.util.List;

public record TableName(String value) {
    public TableName {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Table name cannot be null or blank");
        }
    }

    public static TableName of(String value) {
        return new TableName(value.toUpperCase().trim());
    }

    @Override
    public String toString() {
        return value;
    }
}
