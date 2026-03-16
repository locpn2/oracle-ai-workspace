package com.oracleai.domain.valueobject;

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

    public static ConnectionId of(String value) {
        return new ConnectionId(UUID.fromString(value));
    }
}
