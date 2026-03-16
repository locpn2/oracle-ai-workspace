package com.oracleai.domain.event;

import java.time.Instant;
import java.util.UUID;

public record UserLoggedInEvent(UUID userId, String token, Instant occurredAt) implements DomainEvent {
    public UserLoggedInEvent(UUID userId, String token) {
        this(userId, token, Instant.now());
    }
}
