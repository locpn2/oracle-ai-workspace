package com.oracleai.workspace.auth.domain.valueobject;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class EmailTest {

    @Test
    void createEmail_WithValidValue_ReturnsEmail() {
        Email email = new Email("test@example.com");
        assertEquals("test@example.com", email.value());
    }

    @Test
    void createEmail_WithNull_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> new Email(null));
    }

    @Test
    void createEmail_WithBlank_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> new Email("   "));
    }

    @Test
    void createEmail_WithInvalidFormat_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> new Email("invalid"));
        assertThrows(IllegalArgumentException.class, () -> new Email("invalid@"));
        assertThrows(IllegalArgumentException.class, () -> new Email("@example.com"));
    }

    @Test
    void of_WithWhitespaceAndMixedCase_TrimsAndLowers() {
        Email email = Email.of("  Test@Example.COM  ");
        assertEquals("test@example.com", email.value());
    }
}
