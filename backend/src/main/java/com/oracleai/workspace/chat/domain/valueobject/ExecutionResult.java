package com.oracleai.workspace.chat.domain.valueobject;

import java.util.List;
import java.util.Map;
import java.util.Set;

public record ExecutionResult(
    boolean success,
    int rowCount,
    List<String> columns,
    List<Map<String, Object>> data,
    String errorMessage
) {
    public static ExecutionResult success(List<String> columns, List<Map<String, Object>> data) {
        return new ExecutionResult(true, data.size(), columns, data, null);
    }

    public static ExecutionResult failure(String errorMessage) {
        return new ExecutionResult(false, 0, List.of(), List.of(), errorMessage);
    }

    public boolean isSuccess() {
        return success;
    }
}
