package com.oracleai.workspace.auth.infrastructure.persistence;

import com.oracleai.workspace.auth.domain.entity.User;
import com.oracleai.workspace.auth.domain.valueobject.Email;
import com.oracleai.workspace.auth.domain.valueobject.HashedPassword;
import com.oracleai.workspace.auth.domain.valueobject.Role;
import com.oracleai.workspace.auth.domain.valueobject.UserId;
import com.oracleai.workspace.auth.domain.valueobject.UserStatus;
import com.oracleai.workspace.auth.domain.valueobject.Username;
import jakarta.persistence.*;
import java.time.Instant;
import java.util.Set;
import java.util.UUID;

@Entity
@Table(name = "users")
public class UserEntity {

    @Id
    @Column(name = "id")
    private UUID id;

    @Column(name = "username", unique = true, nullable = false, length = 50)
    private String username;

    @Column(name = "email", unique = true, nullable = false, length = 255)
    private String email;

    @Column(name = "password", nullable = false)
    private String password;

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "user_roles", joinColumns = @JoinColumn(name = "user_id"))
    @Column(name = "role")
    @Enumerated(EnumType.STRING)
    private Set<Role> roles;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false)
    private UserStatus status;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    @Column(name = "last_login_at")
    private Instant lastLoginAt;

    public UserEntity() {}

    public static UserEntity fromDomain(User user) {
        UserEntity entity = new UserEntity();
        entity.id = user.getId().value();
        entity.username = user.getUsername().value();
        entity.email = user.getEmail().value();
        entity.password = user.getPassword().value();
        entity.roles = user.getRoles();
        entity.status = user.getStatus();
        entity.createdAt = user.getCreatedAt();
        entity.lastLoginAt = user.getLastLoginAt().orElse(null);
        return entity;
    }

    public User toDomain() {
        return User.builder()
                .id(UserId.from(this.id.toString()))
                .username(new Username(this.username))
                .email(new Email(this.email))
                .password(new HashedPassword(this.password))
                .roles(this.roles)
                .status(this.status)
                .createdAt(this.createdAt)
                .lastLoginAt(this.lastLoginAt)
                .build();
    }

    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public Set<Role> getRoles() { return roles; }
    public void setRoles(Set<Role> roles) { this.roles = roles; }
    public UserStatus getStatus() { return status; }
    public void setStatus(UserStatus status) { this.status = status; }
    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
    public Instant getLastLoginAt() { return lastLoginAt; }
    public void setLastLoginAt(Instant lastLoginAt) { this.lastLoginAt = lastLoginAt; }
}
