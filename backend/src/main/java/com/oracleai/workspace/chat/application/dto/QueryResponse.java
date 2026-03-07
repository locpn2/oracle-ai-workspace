package com.oracleai.workspace.chat.application.dto;

import java.util.List;
import java.util.Map;

public record QueryResponse(
    String sessionId,
    String message,
    String sql,
    boolean success,
    int rowCount,
    List<String> columns,
    List<Map<String, Object>> data,
    String errorMessage,
    String provider
) {
    public static QueryResponse error(String sessionId, String message, String errorMessage) {
        return new QueryResponse(sessionId, message, null, false, 0, null, null, errorMessage, null);
    }

    public static QueryResponse success(String sessionId, String message, String sql, 
            int rowCount, List<String> columns, List<Map<String, Object>> data, String provider) {
        return new QueryResponse(sessionId, message, sql, true, rowCount, columns, data, null, provider);
    }
}
