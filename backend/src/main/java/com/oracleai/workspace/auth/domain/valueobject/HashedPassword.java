package com.oracleai.workspace.auth.domain.valueobject;

import java.util.Set;

public record HashedPassword(String value) {
    private static final Set<String> COMMON_PASSWORDS = Set.of(
        "password", "12345678", "qwerty", "admin", "letmein",
        "welcome", "monkey", "1234567890"
    );

    public static HashedPassword fromPlain(String plain) {
        if (plain == null || plain.length() < 8) {
            throw new IllegalArgumentException("Password must be at least 8 characters");
        }
        if (!plain.matches(".*[A-Z].*")) {
            throw new IllegalArgumentException("Password must contain at least one uppercase letter");
        }
        if (!plain.matches(".*[a-z].*")) {
            throw new IllegalArgumentException("Password must contain at least one lowercase letter");
        }
        if (!plain.matches(".*\\d.*")) {
            throw new IllegalArgumentException("Password must contain at least one digit");
        }
        if (COMMON_PASSWORDS.contains(plain.toLowerCase())) {
            throw new IllegalArgumentException("Password is too common, choose a stronger one");
        }
        
        // TODO: Integrate BCrypt library (org.mindrot:jbcrypt)
        // String hashed = BCrypt.hashpw(plain, BCrypt.gensalt());
        String hashed = "bcrypt:" + plain.hashCode();
        return new HashedPassword(hashed);
    }

    public boolean matches(String plain) {
        // TODO: Use BCrypt.checkpw when library is available
        // return BCrypt.checkpw(plain, this.value);
        return ("bcrypt:" + plain.hashCode()).equals(this.value);
    }
}
