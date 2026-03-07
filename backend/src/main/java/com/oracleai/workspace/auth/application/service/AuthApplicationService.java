package com.oracleai.workspace.auth.application.service;

import com.oracleai.workspace.auth.application.dto.AuthResponse;
import com.oracleai.workspace.auth.application.dto.LoginRequest;
import com.oracleai.workspace.auth.application.dto.RegisterRequest;
import com.oracleai.workspace.auth.application.port.in.AuthUseCase;
import com.oracleai.workspace.auth.domain.entity.User;
import com.oracleai.workspace.auth.domain.repository.UserRepository;
import com.oracleai.workspace.auth.domain.valueobject.Email;
import com.oracleai.workspace.auth.domain.valueobject.HashedPassword;
import com.oracleai.workspace.auth.domain.valueobject.Role;
import com.oracleai.workspace.auth.domain.valueobject.UserId;
import com.oracleai.workspace.auth.domain.valueobject.Username;
import com.oracleai.workspace.auth.infrastructure.security.JwtUtil;
import com.oracleai.workspace.shared.exception.ValidationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.Instant;
import java.util.Set;

@Service
public class AuthApplicationService implements AuthUseCase {

    private static final Logger log = LoggerFactory.getLogger(AuthApplicationService.class);

    private final UserRepository userRepository;
    private final JwtUtil jwtUtil;

    public AuthApplicationService(UserRepository userRepository, JwtUtil jwtUtil) {
        this.userRepository = userRepository;
        this.jwtUtil = jwtUtil;
    }

    @Override
    @Transactional
    public AuthResponse login(LoginRequest request) {
        log.info("Login attempt for username: {}", request.username());
        
        Username username = new Username(request.username());
        User user = userRepository.findByUsername(username)
                .orElseThrow(() -> new ValidationException("Invalid username or password"));
        
        // Invariant: Password must match
        if (!user.getPassword().matches(request.password())) {
            throw new ValidationException("Invalid username or password");
        }
        
        // Invariant: User must be active
        if (!user.isActive()) {
            throw new ValidationException("User account is not active");
        }
        
        user.recordLogin();
        userRepository.save(user);
        
        String token = jwtUtil.generateToken(user.getUsername().value(), user.getId());
        
        log.info("Login successful for username: {}", request.username());
        return AuthResponse.of(
                token,
                user.getUsername().value(),
                user.getEmail().value(),
                user.getRoles().stream().map(Role::name).collect(java.util.stream.Collectors.toSet()),
                jwtUtil.getExpiration()
        );
    }

    @Override
    @Transactional
    public AuthResponse register(RegisterRequest request) {
        log.info("Registration attempt for username: {}", request.username());
        
        // Invariant: A1 - Username must be unique
        Username username = new Username(request.username());
        if (userRepository.existsByUsername(username)) {
            throw new ValidationException("username", "Username already exists");
        }
        
        // Invariant: A2 - Email must be unique
        Email email = new Email(request.email());
        if (userRepository.existsByEmail(email)) {
            throw new ValidationException("email", "Email already exists");
        }
        
        // Invariant: A3 - At least one role (default: USER)
        Set<Role> roles = Set.of(Role.USER);
        
        // Create new user with hashed password
        HashedPassword hashedPassword = HashedPassword.fromPlain(request.password());
        
        User user = User.builder()
                .id(UserId.generate())
                .username(username)
                .email(email)
                .password(hashedPassword)
                .roles(roles)
                .build();
        
        user = userRepository.save(user);
        
        String token = jwtUtil.generateToken(user.getUsername().value(), user.getId());
        
        log.info("Registration successful for username: {}", request.username());
        return AuthResponse.of(
                token,
                user.getUsername().value(),
                user.getEmail().value(),
                user.getRoles().stream().map(Role::name).collect(java.util.stream.Collectors.toSet()),
                jwtUtil.getExpiration()
        );
    }

    @Override
    public AuthResponse refreshToken(String token) {
        log.info("Token refresh attempt");
        
        if (!jwtUtil.validateToken(token)) {
            throw new ValidationException("Invalid or expired token");
        }
        
        String username = jwtUtil.getUsernameFromToken(token);
        UserId userId = jwtUtil.getUserIdFromToken(token);
        
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new ValidationException("User not found"));
        
        String newToken = jwtUtil.generateToken(user.getUsername().value(), user.getId());
        
        log.info("Token refresh successful for username: {}", username);
        return AuthResponse.of(
                newToken,
                user.getUsername().value(),
                user.getEmail().value(),
                user.getRoles().stream().map(Role::name).collect(java.util.stream.Collectors.toSet()),
                jwtUtil.getExpiration()
        );
    }
}
