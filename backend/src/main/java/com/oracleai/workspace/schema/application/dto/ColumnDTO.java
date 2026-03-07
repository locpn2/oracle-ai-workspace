package com.oracleai.workspace.schema.application.dto;

public record ColumnDTO(
    String name,
    String dataType,
    boolean nullable,
    int position,
    String defaultValue
) {}
