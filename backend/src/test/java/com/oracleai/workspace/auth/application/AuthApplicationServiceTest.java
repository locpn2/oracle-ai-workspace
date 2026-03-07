package com.oracleai.workspace.auth.application;

import com.oracleai.workspace.auth.application.dto.AuthResponse;
import com.oracleai.workspace.auth.application.dto.LoginRequest;
import com.oracleai.workspace.auth.application.dto.RegisterRequest;
import com.oracleai.workspace.auth.application.service.AuthApplicationService;
import com.oracleai.workspace.auth.domain.entity.User;
import com.oracleai.workspace.auth.domain.repository.UserRepository;
import com.oracleai.workspace.auth.domain.valueobject.*;
import com.oracleai.workspace.auth.infrastructure.security.JwtUtil;
import com.oracleai.workspace.shared.exception.ValidationException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AuthApplicationServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private JwtUtil jwtUtil;

    private AuthApplicationService authService;

    @BeforeEach
    void setUp() {
        authService = new AuthApplicationService(userRepository, jwtUtil);
    }

    @Test
    void login_WithValidCredentials_ReturnsAuthResponse() {
        Username username = new Username("testuser");
        User user = User.builder()
                .id(UserId.generate())
                .username(username)
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER))
                .status(UserStatus.ACTIVE)
                .build();

        when(userRepository.findByUsername(username)).thenReturn(Optional.of(user));
        when(jwtUtil.generateToken(any(), any())).thenReturn("test-token");
        when(jwtUtil.getExpiration()).thenReturn(3600000L);

        LoginRequest request = new LoginRequest("testuser", "SecurePass123");
        AuthResponse response = authService.login(request);

        assertNotNull(response);
        assertEquals("test-token", response.token());
        assertEquals("testuser", response.username());
        verify(userRepository).save(any(User.class));
    }

    @Test
    void login_WithInvalidUsername_ThrowsException() {
        Username username = new Username("nonexistent");
        when(userRepository.findByUsername(username)).thenReturn(Optional.empty());

        LoginRequest request = new LoginRequest("nonexistent", "SecurePass123");

        assertThrows(ValidationException.class, () -> authService.login(request));
    }

    @Test
    void login_WithInvalidPassword_ThrowsException() {
        Username username = new Username("testuser");
        User user = User.builder()
                .id(UserId.generate())
                .username(username)
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER))
                .status(UserStatus.ACTIVE)
                .build();

        when(userRepository.findByUsername(username)).thenReturn(Optional.of(user));

        LoginRequest request = new LoginRequest("testuser", "WrongPassword");

        assertThrows(ValidationException.class, () -> authService.login(request));
    }

    @Test
    void login_WithInactiveUser_ThrowsException() {
        Username username = new Username("testuser");
        User user = User.builder()
                .id(UserId.generate())
                .username(username)
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER))
                .status(UserStatus.LOCKED)
                .build();

        when(userRepository.findByUsername(username)).thenReturn(Optional.of(user));

        LoginRequest request = new LoginRequest("testuser", "SecurePass123");

        assertThrows(ValidationException.class, () -> authService.login(request));
    }

    @Test
    void register_WithNewUsername_ReturnsAuthResponse() {
        when(userRepository.existsByUsername(any())).thenReturn(false);
        when(userRepository.existsByEmail(any())).thenReturn(false);
        when(userRepository.save(any(User.class))).thenAnswer(inv -> inv.getArgument(0));
        when(jwtUtil.generateToken(any(), any())).thenReturn("test-token");
        when(jwtUtil.getExpiration()).thenReturn(3600000L);

        RegisterRequest request = new RegisterRequest("newuser", "newuser@example.com", "SecurePass123");
        AuthResponse response = authService.register(request);

        assertNotNull(response);
        assertEquals("newuser", response.username());
        assertEquals("newuser@example.com", response.email());
        verify(userRepository).save(any(User.class));
    }

    @Test
    void register_WithExistingUsername_ThrowsException() {
        when(userRepository.existsByUsername(any())).thenReturn(true);

        RegisterRequest request = new RegisterRequest("existinguser", "new@example.com", "SecurePass123");

        assertThrows(ValidationException.class, () -> authService.register(request));
    }

    @Test
    void register_WithExistingEmail_ThrowsException() {
        when(userRepository.existsByUsername(any())).thenReturn(false);
        when(userRepository.existsByEmail(any())).thenReturn(true);

        RegisterRequest request = new RegisterRequest("newuser", "existing@example.com", "SecurePass123");

        assertThrows(ValidationException.class, () -> authService.register(request));
    }

    @Test
    void refreshToken_WithValidToken_ReturnsNewAuthResponse() {
        String token = "valid-token";
        Username username = new Username("testuser");
        UserId userId = UserId.generate();

        User user = User.builder()
                .id(userId)
                .username(username)
                .email(new Email("test@example.com"))
                .password(HashedPassword.fromPlain("SecurePass123"))
                .roles(Set.of(Role.USER))
                .status(UserStatus.ACTIVE)
                .build();

        when(jwtUtil.validateToken(token)).thenReturn(true);
        when(jwtUtil.getUsernameFromToken(token)).thenReturn("testuser");
        when(jwtUtil.getUserIdFromToken(token)).thenReturn(userId);
        when(userRepository.findById(userId)).thenReturn(Optional.of(user));
        when(jwtUtil.generateToken(any(), any())).thenReturn("new-token");
        when(jwtUtil.getExpiration()).thenReturn(3600000L);

        AuthResponse response = authService.refreshToken(token);

        assertNotNull(response);
        assertEquals("new-token", response.token());
    }

    @Test
    void refreshToken_WithInvalidToken_ThrowsException() {
        String token = "invalid-token";
        when(jwtUtil.validateToken(token)).thenReturn(false);

        assertThrows(ValidationException.class, () -> authService.refreshToken(token));
    }
}
