package com.oracleai.workspace.vector.application.dto;

import java.util.List;
import java.util.Map;

public record SearchResponse(
    String query,
    int totalResults,
    List<SearchHit> hits
) {
    public record SearchHit(
        String tableName,
        String rowId,
        String document,
        double similarityScore
    ) {}
}
