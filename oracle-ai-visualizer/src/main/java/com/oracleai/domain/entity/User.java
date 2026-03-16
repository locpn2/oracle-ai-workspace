package com.oracleai.domain.entity;

import com.oracleai.domain.valueobject.*;
import java.time.Instant;
import java.util.UUID;

public class User {
    private UserId id;
    private Username username;
    private EncryptedPassword password;
    private UserRole role;
    private CreatedAt createdAt;

    private User() {}

    public User(UserId id, Username username, EncryptedPassword password, UserRole role, CreatedAt createdAt) {
        this.id = id;
        this.username = username;
        this.password = password;
        this.role = role;
        this.createdAt = createdAt;
    }

    public static User create(String username, String password, UserRole role) {
        return new User(
            UserId.generate(),
            new Username(username),
            new EncryptedPassword(password),
            role,
            CreatedAt.now()
        );
    }

    public void changePassword(String newPassword, PasswordEncoder encoder) {
        if (newPassword == null || newPassword.length() < 8) {
            throw new IllegalArgumentException("Password must be at least 8 characters");
        }
        this.password = new EncryptedPassword(encoder.encode(newPassword));
    }

    public boolean canAccess(String resource) {
        return role.canAccess(resource);
    }

    public UserId getId() { return id; }
    public Username getUsername() { return username; }
    public EncryptedPassword getPassword() { return password; }
    public UserRole getRole() { return role; }
    public CreatedAt getCreatedAt() { return createdAt; }

    public interface PasswordEncoder {
        String encode(String rawPassword);
    }
}
