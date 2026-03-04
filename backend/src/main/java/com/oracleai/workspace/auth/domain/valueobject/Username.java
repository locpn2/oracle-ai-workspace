package com.oracleai.workspace.auth.domain.valueobject;

public record Username(String value) {
    public Username {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Username cannot be null or blank");
        }
        if (value.length() < 3) {
            throw new IllegalArgumentException("Username must be at least 3 characters");
        }
        if (!value.matches("^[a-zA-Z0-9_]+$")) {
            throw new IllegalArgumentException("Username can only contain alphanumeric and underscore");
        }
    }

    public static Username of(String value) {
        return new Username(value.trim().toLowerCase());
    }
}
