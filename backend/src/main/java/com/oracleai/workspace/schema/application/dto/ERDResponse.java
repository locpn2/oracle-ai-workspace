package com.oracleai.workspace.schema.application.dto;

import java.util.List;
import java.util.Map;

public record ERDResponse(
    List<TableDTO> tables,
    List<RelationshipDTO> relationships,
    Map<String, Object> metadata
) {
    public record RelationshipDTO(
        String fromTable,
        String toTable,
        List<String> fromColumns,
        List<String> toColumns
    ) {}
}
