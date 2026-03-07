package com.oracleai.workspace.auth.api;

import com.oracleai.workspace.auth.application.dto.AuthResponse;
import com.oracleai.workspace.auth.application.dto.LoginRequest;
import com.oracleai.workspace.auth.application.dto.RegisterRequest;
import com.oracleai.workspace.auth.application.port.in.AuthUseCase;
import com.oracleai.workspace.shared.dto.ApiResponse;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private static final Logger log = LoggerFactory.getLogger(AuthController.class);

    private final AuthUseCase authUseCase;

    public AuthController(AuthUseCase authUseCase) {
        this.authUseCase = authUseCase;
    }

    @PostMapping("/login")
    public ResponseEntity<ApiResponse<AuthResponse>> login(@Valid @RequestBody LoginRequest request) {
        log.info("Login request for username: {}", request.username());
        AuthResponse response = authUseCase.login(request);
        return ResponseEntity.ok(ApiResponse.success(response, "Login successful"));
    }

    @PostMapping("/register")
    public ResponseEntity<ApiResponse<AuthResponse>> register(@Valid @RequestBody RegisterRequest request) {
        log.info("Register request for username: {}", request.username());
        AuthResponse response = authUseCase.register(request);
        return ResponseEntity.ok(ApiResponse.success(response, "Registration successful"));
    }

    @PostMapping("/refresh")
    public ResponseEntity<ApiResponse<AuthResponse>> refreshToken(@RequestHeader("Authorization") String authHeader) {
        log.info("Token refresh request");
        String token = authHeader.replace("Bearer ", "");
        AuthResponse response = authUseCase.refreshToken(token);
        return ResponseEntity.ok(ApiResponse.success(response, "Token refreshed"));
    }

    @GetMapping("/me")
    public ResponseEntity<ApiResponse<AuthResponse>> getCurrentUser() {
        // In a real implementation, get user from security context
        return ResponseEntity.ok(ApiResponse.success(null, "Current user info"));
    }
}
