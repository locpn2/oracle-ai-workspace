package com.oracleai.workspace.chat.domain.valueobject;

import java.util.Set;

public record ValidatedSQL(
    String sql,
    SQLType type,
    Set<String> referencedTables,
    Set<String> referencedColumns
) {
    public boolean isValid() {
        return sql != null && !sql.isBlank() && type != null;
    }

    public boolean referencesTable(String tableName) {
        return referencedTables.contains(tableName.toUpperCase());
    }
}
