package com.oracleai.domain.valueobject;

public enum UserRole {
    ADMIN,
    USER,
    VIEWER;

    public boolean canAccess(String resource) {
        return switch (this) {
            case ADMIN -> true;
            case USER -> !resource.startsWith("/admin");
            case VIEWER -> resource.startsWith("/view") || resource.startsWith("/schema");
        };
    }
}
