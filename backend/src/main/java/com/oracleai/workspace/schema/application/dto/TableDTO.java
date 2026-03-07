package com.oracleai.workspace.schema.application.dto;

import java.util.List;

public record TableDTO(
    String name,
    String type,
    List<ColumnDTO> columns,
    PrimaryKeyDTO primaryKey,
    List<ForeignKeyDTO> foreignKeys
) {
    public record PrimaryKeyDTO(
        String name,
        List<String> columns
    ) {}

    public record ForeignKeyDTO(
        String name,
        List<String> sourceColumns,
        String targetTable,
        List<String> targetColumns,
        String deleteRule
    ) {}
}
