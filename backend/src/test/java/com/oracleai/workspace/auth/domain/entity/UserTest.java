package com.oracleai.workspace.auth.domain.entity;

import com.oracleai.workspace.auth.domain.valueobject.*;
import org.junit.jupiter.api.Test;

import java.time.Instant;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class UserTest {

    @Test
    void createUser_WithValidData_ReturnsUser() {
        User user = User.builder()
                .username(new Username("testuser"))
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER))
                .build();

        assertNotNull(user);
        assertEquals("testuser", user.getUsername().value());
        assertEquals("test@example.com", user.getEmail().value());
        assertTrue(user.isActive());
    }

    @Test
    void createUser_WithoutUsername_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () ->
                User.builder()
                        .email(new Email("test@example.com"))
                        .password(HashedPassword.fromPlain("SecurePass123"))
                        .roles(Set.of(Role.USER))
                        .build()
        );
    }

    @Test
    void createUser_WithoutRoles_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () ->
                User.builder()
                        .username(new Username("testuser"))
                        .email(new Email("test@example.com"))
                        .password(HashedPassword.fromPlain("SecurePass123"))
                        .roles(Set.of())
                        .build()
        );
    }

    @Test
    void changePassword_WithCorrectCurrentPassword_ChangesPassword() {
        User user = User.builder()
                .username(new Username("testuser"))
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("OldPass123"))
                .build();

        user.changePassword("OldPass123", "NewPass456");

        assertTrue(user.getPassword().matches("NewPass456"));
    }

    @Test
    void changePassword_WithIncorrectCurrentPassword_ThrowsException() {
        User user = User.builder()
                .username(new Username("testuser"))
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("OldPass123"))
                .build();

        assertThrows(User.InvalidPasswordException.class, () ->
                user.changePassword("wrongpassword", "newpassword")
        );
    }

    @Test
    void assignRole_AddsRoleToUser() {
        User user = User.builder()
                .username(new Username("testuser"))
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER))
                .build();

        user.assignRole(Role.ADMIN);

        assertTrue(user.getRoles().contains(Role.ADMIN));
    }

    @Test
    void removeRole_WithMultipleRoles_RemovesRole() {
        User user = User.builder()
                .username(new Username("testuser"))
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER, Role.ADMIN))
                .build();

        user.removeRole(Role.ADMIN);

        assertFalse(user.getRoles().contains(Role.ADMIN));
        assertTrue(user.getRoles().contains(Role.USER));
    }

    @Test
    void removeRole_WithOnlyOneRole_ThrowsException() {
        User user = User.builder()
                .username(new Username("testuser"))
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER))
                .build();

        assertThrows(IllegalStateException.class, () ->
                user.removeRole(Role.USER)
        );
    }

    @Test
    void hasPermission_ActiveAdminUser_ReturnsTrue() {
        User user = User.builder()
                .username(new Username("admin"))
                .email(new Email("admin@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.ADMIN))
                .status(UserStatus.ACTIVE)
                .build();

        assertTrue(user.hasPermission(Permission.SCHEMA_READ));
        assertTrue(user.hasPermission(Permission.USER_MANAGE));
    }

    @Test
    void hasPermission_InactiveUser_ReturnsFalse() {
        User user = User.builder()
                .username(new Username("testuser"))
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.ADMIN))
                .status(UserStatus.LOCKED)
                .build();

        assertFalse(user.hasPermission(Permission.SCHEMA_READ));
    }

    @Test
    void hasPermission_ViewerRole_CanOnlyReadSchemaAndChat() {
        User user = User.builder()
                .username(new Username("viewer"))
                .email(new Email("viewer@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.VIEWER))
                .status(UserStatus.ACTIVE)
                .build();

        assertTrue(user.hasPermission(Permission.SCHEMA_READ));
        assertTrue(user.hasPermission(Permission.CHAT_QUERY));
        assertFalse(user.hasPermission(Permission.SCHEMA_WRITE));
    }

    @Test
    void lock_ChangesStatusToLocked() {
        User user = User.builder()
                .username(new Username("testuser"))
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER))
                .status(UserStatus.ACTIVE)
                .build();

        user.lock();

        assertEquals(UserStatus.LOCKED, user.getStatus());
        assertFalse(user.isActive());
    }

    @Test
    void unlock_ChangesStatusToActive() {
        User user = User.builder()
                .username(new Username("testuser"))
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER))
                .status(UserStatus.LOCKED)
                .build();

        user.unlock();

        assertEquals(UserStatus.ACTIVE, user.getStatus());
        assertTrue(user.isActive());
    }

    @Test
    void recordLogin_UpdatesLastLoginAt() {
        User user = User.builder()
                .username(new Username("testuser"))
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER))
                .build();

        assertFalse(user.getLastLoginAt().isPresent());
        
        user.recordLogin();

        assertTrue(user.getLastLoginAt().isPresent());
    }
}
