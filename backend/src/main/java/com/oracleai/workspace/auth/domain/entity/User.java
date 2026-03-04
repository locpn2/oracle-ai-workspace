package com.oracleai.workspace.auth.domain.entity;

import com.oracleai.workspace.auth.domain.valueobject.*;
import java.time.Instant;
import java.util.*;

public final class User {
    private final UserId id;
    private final Username username;
    private HashedPassword password;
    private final Email email;
    private final Set<Role> roles;
    private UserStatus status;
    private final Instant createdAt;
    private Instant lastLoginAt;

    private User(Builder builder) {
        this.id = builder.id;
        this.username = builder.username;
        this.password = builder.password;
        this.email = builder.email;
        this.roles = new HashSet<>(builder.roles);
        this.status = builder.status;
        this.createdAt = builder.createdAt;
    }

    public UserId getId() {
        return id;
    }

    public Username getUsername() {
        return username;
    }

    public Email getEmail() {
        return email;
    }

    public Set<Role> getRoles() {
        return Set.copyOf(roles);
    }

    public UserStatus getStatus() {
        return status;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public Optional<Instant> getLastLoginAt() {
        return Optional.ofNullable(lastLoginAt);
    }

    public void changePassword(String currentPassword, String newPassword) {
        if (!this.password.matches(currentPassword)) {
            throw new InvalidPasswordException("Current password is incorrect");
        }
        this.password = HashedPassword.fromPlain(newPassword);
    }

    public void assignRole(Role role) {
        this.roles.add(role);
    }

    public void removeRole(Role role) {
        if (roles.size() == 1 && roles.contains(role)) {
            throw new IllegalStateException("User must have at least one role");
        }
        this.roles.remove(role);
    }

    public boolean hasPermission(Permission permission) {
        if (status != UserStatus.ACTIVE) {
            return false;
        }
        
        for (Role role : roles) {
            if (hasPermissionByRole(role, permission)) {
                return true;
            }
        }
        return false;
    }

    private boolean hasPermissionByRole(Role role, Permission permission) {
        return switch (role) {
            case ADMIN -> true;
            case USER -> permission != Permission.USER_MANAGE;
            case VIEWER -> permission == Permission.SCHEMA_READ || 
                         permission == Permission.CHAT_QUERY;
        };
    }

    public void lock() {
        this.status = UserStatus.LOCKED;
    }

    public void unlock() {
        this.status = UserStatus.ACTIVE;
    }

    public void suspend() {
        this.status = UserStatus.SUSPENDED;
    }

    public void recordLogin() {
        this.lastLoginAt = Instant.now();
    }

    public boolean isActive() {
        return status == UserStatus.ACTIVE;
    }

    public record UserId(java.util.UUID value) {
        public UserId {
            if (value == null) {
                throw new IllegalArgumentException("User ID cannot be null");
            }
        }

        public static UserId generate() {
            return new UserId(java.util.UUID.randomUUID());
        }
    }

    public static class InvalidPasswordException extends RuntimeException {
        public InvalidPasswordException(String message) {
            super(message);
        }
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private UserId id = UserId.generate();
        private Username username;
        private HashedPassword password;
        private Email email;
        private Set<Role> roles = Set.of(Role.USER);
        private UserStatus status = UserStatus.ACTIVE;
        private Instant createdAt = Instant.now();

        public Builder id(UserId id) {
            this.id = id;
            return this;
        }

        public Builder username(Username username) {
            this.username = username;
            return this;
        }

        public Builder password(HashedPassword password) {
            this.password = password;
            return this;
        }

        public Builder email(Email email) {
            this.email = email;
            return this;
        }

        public Builder roles(Set<Role> roles) {
            this.roles = roles;
            return this;
        }

        public Builder addRole(Role role) {
            this.roles.add(role);
            return this;
        }

        public Builder status(UserStatus status) {
            this.status = status;
            return this;
        }

        public User build() {
            if (username == null) {
                throw new IllegalArgumentException("Username is required");
            }
            if (password == null) {
                throw new IllegalArgumentException("Password is required");
            }
            if (email == null) {
                throw new IllegalArgumentException("Email is required");
            }
            if (roles.isEmpty()) {
                throw new IllegalArgumentException("User must have at least one role");
            }
            return new User(this);
        }
    }
}
