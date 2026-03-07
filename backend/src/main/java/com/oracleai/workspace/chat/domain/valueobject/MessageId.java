package com.oracleai.workspace.chat.domain.valueobject;

import java.util.UUID;

public record MessageId(UUID value) {
    public MessageId {
        if (value == null) {
            throw new IllegalArgumentException("MessageId cannot be null");
        }
    }

    public static MessageId generate() {
        return new MessageId(UUID.randomUUID());
    }

    public static MessageId from(String value) {
        return new MessageId(UUID.fromString(value));
    }

    @Override
    public String toString() {
        return value.toString();
    }
}
