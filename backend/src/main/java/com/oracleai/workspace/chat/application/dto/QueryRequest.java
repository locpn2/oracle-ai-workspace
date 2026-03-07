package com.oracleai.workspace.chat.application.dto;

import jakarta.validation.constraints.NotBlank;

public record QueryRequest(
    @NotBlank(message = "Message is required")
    String message,
    String sessionId
) {}
