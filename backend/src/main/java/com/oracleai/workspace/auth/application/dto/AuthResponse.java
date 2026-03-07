package com.oracleai.workspace.auth.application.dto;

import java.util.Set;

public record AuthResponse(
    String token,
    String type,
    String username,
    String email,
    Set<String> roles,
    long expiresIn
) {
    public static AuthResponse of(String token, String username, String email, Set<String> roles, long expiresIn) {
        return new AuthResponse(token, "Bearer", username, email, roles, expiresIn);
    }
}
