package com.oracleai.workspace.auth.domain.valueobject;

import java.util.UUID;

public record ConnectionId(UUID value) {
    public ConnectionId {
        if (value == null) {
            throw new IllegalArgumentException("ConnectionId cannot be null");
        }
    }

    public static ConnectionId generate() {
        return new ConnectionId(UUID.randomUUID());
    }

    public static ConnectionId from(String value) {
        return new ConnectionId(UUID.fromString(value));
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
