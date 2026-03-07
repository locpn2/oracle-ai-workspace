package com.oracleai.workspace.schema.domain.valueobject;

import java.util.UUID;

public record SchemaId(UUID value) {
    public SchemaId {
        if (value == null) {
            throw new IllegalArgumentException("SchemaId cannot be null");
        }
    }

    public static SchemaId generate() {
        return new SchemaId(UUID.randomUUID());
    }

    public static SchemaId from(String value) {
        return new SchemaId(UUID.fromString(value));
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
