package com.oracleai.workspace.chat.domain.entity;

import com.oracleai.workspace.chat.domain.valueobject.*;
import java.time.Instant;
import java.util.UUID;

public final class ChatMessage {
    private final MessageId id;
    private final MessageRole role;
    private final String content;
    private final String sql;
    private final Instant timestamp;
    private final ExecutionResult result;

    private ChatMessage(Builder builder) {
        this.id = builder.id;
        this.role = builder.role;
        this.content = builder.content;
        this.sql = builder.sql;
        this.timestamp = builder.timestamp;
        this.result = builder.result;
    }

    public MessageId getId() {
        return id;
    }

    public MessageRole getRole() {
        return role;
    }

    public String getContent() {
        return content;
    }

    public String getSql() {
        return sql;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public ExecutionResult getResult() {
        return result;
    }

    public boolean hasSQL() {
        return sql != null && !sql.isBlank();
    }

    public boolean isSuccessful() {
        return result != null && result.isSuccess();
    }

    public boolean isUserMessage() {
        return role == MessageRole.USER;
    }

    public boolean isAssistantMessage() {
        return role == MessageRole.ASSISTANT;
    }

    public record MessageId(UUID value) {
        public MessageId {
            if (value == null) {
                throw new IllegalArgumentException("Message ID cannot be null");
            }
        }

        public static MessageId generate() {
            return new MessageId(UUID.randomUUID());
        }
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private MessageId id = MessageId.generate();
        private MessageRole role;
        private String content;
        private String sql;
        private Instant timestamp = Instant.now();
        private ExecutionResult result;

        public Builder id(MessageId id) {
            this.id = id;
            return this;
        }

        public Builder role(MessageRole role) {
            this.role = role;
            return this;
        }

        public Builder content(String content) {
            this.content = content;
            return this;
        }

        public Builder sql(String sql) {
            this.sql = sql;
            return this;
        }

        public Builder timestamp(Instant timestamp) {
            this.timestamp = timestamp;
            return this;
        }

        public Builder result(ExecutionResult result) {
            this.result = result;
            return this;
        }

        public ChatMessage build() {
            if (role == null) {
                throw new IllegalArgumentException("Message role is required");
            }
            if (content == null || content.isBlank()) {
                throw new IllegalArgumentException("Message content is required");
            }
            return new ChatMessage(this);
        }
    }
}
