package com.oracleai.workspace.auth.domain.valueobject;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class HashedPasswordTest {

    @Test
    void fromPlain_WithValidPassword_ReturnsHashedPassword() {
        HashedPassword password = HashedPassword.fromPlain("SecurePass123");
        assertNotNull(password.value());
        assertTrue(password.value().startsWith("bcrypt:"));
    }

    @Test
    void fromPlain_WithNull_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> HashedPassword.fromPlain(null));
    }

    @Test
    void fromPlain_WithShortPassword_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> HashedPassword.fromPlain("Short1"));
    }

    @Test
    void fromPlain_WithoutUppercase_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> HashedPassword.fromPlain("lowercase1"));
    }

    @Test
    void fromPlain_WithoutLowercase_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> HashedPassword.fromPlain("UPPERCASE1"));
    }

    @Test
    void fromPlain_WithoutDigit_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> HashedPassword.fromPlain("NoDigits"));
    }

    @Test
    void fromPlain_WithCommonPassword_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () -> HashedPassword.fromPlain("password"));
        assertThrows(IllegalArgumentException.class, () -> HashedPassword.fromPlain("12345678"));
    }

    @Test
    void matches_WithCorrectPassword_ReturnsTrue() {
        HashedPassword password = HashedPassword.fromPlain("SecurePass123");
        assertTrue(password.matches("SecurePass123"));
    }

    @Test
    void matches_WithWrongPassword_ReturnsFalse() {
        HashedPassword password = HashedPassword.fromPlain("SecurePass123");
        assertFalse(password.matches("WrongPassword"));
    }
}
