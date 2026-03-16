package com.oracleai.domain.event;

import java.time.Instant;
import java.util.UUID;

public record DatabaseConnectedEvent(UUID connectionId, Instant occurredAt) implements DomainEvent {
    public DatabaseConnectedEvent(UUID connectionId) {
        this(connectionId, Instant.now());
    }
}
