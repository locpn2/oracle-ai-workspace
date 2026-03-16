package com.oracleai.application.service;

import com.oracleai.application.dto.AuthResponse;
import com.oracleai.domain.valueobject.UserRole;
import org.springframework.stereotype.Service;

@Service
public class AuthService {
    
    public AuthResponse register(String username, String password) {
        return new AuthResponse("token", username, "USER");
    }
    
    public AuthResponse login(String username, String password) {
        return new AuthResponse("token", username, "USER");
    }
}
