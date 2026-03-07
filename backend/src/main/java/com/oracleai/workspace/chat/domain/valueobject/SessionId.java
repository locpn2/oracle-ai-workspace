package com.oracleai.workspace.chat.domain.valueobject;

import java.util.UUID;

public record SessionId(UUID value) {
    public SessionId {
        if (value == null) {
            throw new IllegalArgumentException("SessionId cannot be null");
        }
    }

    public static SessionId generate() {
        return new SessionId(UUID.randomUUID());
    }

    public static SessionId from(String value) {
        return new SessionId(UUID.fromString(value));
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
