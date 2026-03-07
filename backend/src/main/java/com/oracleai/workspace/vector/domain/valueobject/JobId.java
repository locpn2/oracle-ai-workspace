package com.oracleai.workspace.vector.domain.valueobject;

import java.util.UUID;

public record JobId(UUID value) {
    public JobId {
        if (value == null) {
            throw new IllegalArgumentException("JobId cannot be null");
        }
    }

    public static JobId generate() {
        return new JobId(UUID.randomUUID());
    }

    public static JobId from(String value) {
        return new JobId(UUID.fromString(value));
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
