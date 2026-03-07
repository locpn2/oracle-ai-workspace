package com.oracleai.workspace.schema.domain.valueobject;

import java.util.List;

public record PrimaryKey(
    List<ColumnName> columns,
    ConstraintName name
) {
    public PrimaryKey {
        if (columns == null || columns.isEmpty()) {
            throw new IllegalArgumentException("Primary key must have at least one column");
        }
    }
}
