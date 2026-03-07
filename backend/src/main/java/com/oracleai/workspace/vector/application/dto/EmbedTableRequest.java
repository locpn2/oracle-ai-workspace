package com.oracleai.workspace.vector.application.dto;

import jakarta.validation.constraints.NotBlank;

public record EmbedTableRequest(
    @NotBlank(message = "Table name is required")
    String tableName,
    Integer batchSize
) {}
