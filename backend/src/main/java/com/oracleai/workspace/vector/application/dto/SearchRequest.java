package com.oracleai.workspace.vector.application.dto;

import jakarta.validation.constraints.NotBlank;

public record SearchRequest(
    @NotBlank(message = "Query is required")
    String query,
    String tableName,
    int limit
) {
    public SearchRequest {
        if (limit <= 0) limit = 10;
        if (limit > 100) limit = 100;
    }
}
