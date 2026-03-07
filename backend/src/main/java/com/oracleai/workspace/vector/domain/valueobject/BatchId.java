package com.oracleai.workspace.vector.domain.valueobject;

import java.util.UUID;

public record BatchId(UUID value) {
    public BatchId {
        if (value == null) {
            throw new IllegalArgumentException("BatchId cannot be null");
        }
    }

    public static BatchId generate() {
        return new BatchId(UUID.randomUUID());
    }

    public static BatchId from(String value) {
        return new BatchId(UUID.fromString(value));
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
