package com.oracleai.domain.event;

import java.time.Instant;
import java.util.UUID;

public record UserRegisteredEvent(UUID userId, String username, Instant occurredAt) implements DomainEvent {
    public UserRegisteredEvent(UUID userId, String username) {
        this(userId, username, Instant.now());
    }
}
