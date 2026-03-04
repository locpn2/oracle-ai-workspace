package com.oracleai.workspace.chat.domain.entity;

import com.oracleai.workspace.chat.domain.valueobject.*;
import java.time.Instant;
import java.util.*;

public final class ChatSession {
    private static final int MAX_MESSAGES = 100;
    
    private final SessionId id;
    private final UserId userId;
    private final SchemaId schemaId;
    private final List<ChatMessage> messages;
    private SessionStatus status;
    private final Instant createdAt;
    private Instant lastActivityAt;

    private ChatSession(Builder builder) {
        this.id = builder.id;
        this.userId = builder.userId;
        this.schemaId = builder.schemaId;
        this.messages = new ArrayList<>(builder.messages);
        this.status = builder.status;
        this.createdAt = builder.createdAt;
        this.lastActivityAt = builder.lastActivityAt;
    }

    public SessionId getId() {
        return id;
    }

    public UserId getUserId() {
        return userId;
    }

    public SchemaId getSchemaId() {
        return schemaId;
    }

    public List<ChatMessage> getMessages() {
        return List.copyOf(messages);
    }

    public SessionStatus getStatus() {
        return status;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public Instant getLastActivityAt() {
        return lastActivityAt;
    }

    public void addUserMessage(String content) {
        ensureActive();
        
        ChatMessage message = ChatMessage.builder()
            .role(MessageRole.USER)
            .content(content)
            .build();
        
        messages.add(message);
        updateActivity();
        
        enforceMaxMessages();
    }

    public void addAssistantMessage(String content, String sql, ExecutionResult result) {
        ensureActive();
        
        ChatMessage message = ChatMessage.builder()
            .role(MessageRole.ASSISTANT)
            .content(content)
            .sql(sql)
            .result(result)
            .build();
        
        messages.add(message);
        updateActivity();
        
        enforceMaxMessages();
    }

    public List<ChatMessage> getRecentMessages(int count) {
        int size = messages.size();
        if (count >= size) {
            return getMessages();
        }
        return messages.subList(size - count, size);
    }

    public void close() {
        if (status != SessionStatus.ACTIVE) {
            throw new IllegalStateException("Can only close active session");
        }
        this.status = SessionStatus.CLOSED;
    }

    public void expire() {
        if (status != SessionStatus.ACTIVE) {
            throw new IllegalStateException("Can only expire active session");
        }
        this.status = SessionStatus.EXPIRED;
    }

    private void ensureActive() {
        if (status != SessionStatus.ACTIVE) {
            throw new IllegalStateException("Session is not active: " + status);
        }
    }

    private void updateActivity() {
        this.lastActivityAt = Instant.now();
    }

    private void enforceMaxMessages() {
        while (messages.size() > MAX_MESSAGES) {
            messages.remove(0);
        }
    }

    public record SessionId(UUID value) {
        public SessionId {
            if (value == null) {
                throw new IllegalArgumentException("Session ID cannot be null");
            }
        }

        public static SessionId generate() {
            return new SessionId(UUID.randomUUID());
        }
    }

    public record UserId(UUID value) {
        public UserId {
            if (value == null) {
                throw new IllegalArgumentException("User ID cannot be null");
            }
        }
    }

    public record SchemaId(UUID value) {
        public SchemaId {
            if (value == null) {
                throw new IllegalArgumentException("Schema ID cannot be null");
            }
        }
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private SessionId id = SessionId.generate();
        private UserId userId;
        private SchemaId schemaId;
        private List<ChatMessage> messages = new ArrayList<>();
        private SessionStatus status = SessionStatus.ACTIVE;
        private Instant createdAt = Instant.now();
        private Instant lastActivityAt = Instant.now();

        public Builder id(SessionId id) {
            this.id = id;
            return this;
        }

        public Builder userId(UserId userId) {
            this.userId = userId;
            return this;
        }

        public Builder schemaId(SchemaId schemaId) {
            this.schemaId = schemaId;
            return this;
        }

        public Builder messages(List<ChatMessage> messages) {
            this.messages = messages;
            return this;
        }

        public Builder status(SessionStatus status) {
            this.status = status;
            return this;
        }

        public Builder createdAt(Instant createdAt) {
            this.createdAt = createdAt;
            return this;
        }

        public ChatSession build() {
            if (userId == null) {
                throw new IllegalArgumentException("User ID is required");
            }
            if (schemaId == null) {
                throw new IllegalArgumentException("Schema ID is required");
            }
            return new ChatSession(this);
        }
    }
}
