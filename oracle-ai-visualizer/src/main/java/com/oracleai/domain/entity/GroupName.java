package com.oracleai.domain.entity;

public record GroupName(String value) {
    public GroupName {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Group name cannot be blank");
        }
        if (value.length() > 100) {
            throw new IllegalArgumentException("Group name cannot exceed 100 characters");
        }
    }
}
