package com.oracleai.workspace.auth.domain.valueobject;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class UsernameTest {

    @Test
    void createUsername_WithValidValue_ReturnsUsername() {
        Username username = new Username("testuser");
        assertEquals("testuser", username.value());
    }

    @Test
    void createUsername_WithNull_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> new Username(null));
    }

    @Test
    void createUsername_WithBlank_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> new Username("   "));
    }

    @Test
    void createUsername_WithShortValue_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> new Username("ab"));
    }

    @Test
    void createUsername_WithInvalidChars_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> new Username("user@name"));
        assertThrows(IllegalArgumentException.class, () -> new Username("user-name"));
    }

    @Test
    void createUsername_WithValidSpecialChars_ReturnsUsername() {
        Username username = new Username("user_123");
        assertEquals("user_123", username.value());
    }

    @Test
    void of_WithWhitespace_TrimsAndLowers() {
        Username username = Username.of("  TestUser  ");
        assertEquals("testuser", username.value());
    }
}
