package com.oracleai.workspace.auth.application.port.in;

import com.oracleai.workspace.auth.application.dto.AuthResponse;
import com.oracleai.workspace.auth.application.dto.LoginRequest;
import com.oracleai.workspace.auth.application.dto.RegisterRequest;

public interface AuthUseCase {
    AuthResponse login(LoginRequest request);
    AuthResponse register(RegisterRequest request);
    AuthResponse refreshToken(String token);
}
