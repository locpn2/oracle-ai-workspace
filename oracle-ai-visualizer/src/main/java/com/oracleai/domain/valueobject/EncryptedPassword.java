package com.oracleai.domain.valueobject;

public record EncryptedPassword(String value) {
    public EncryptedPassword {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Password cannot be blank");
        }
    }
}
