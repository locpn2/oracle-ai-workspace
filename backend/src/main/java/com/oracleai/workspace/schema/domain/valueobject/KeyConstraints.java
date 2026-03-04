package com.oracleai.workspace.schema.domain.valueobject;

import java.util.List;

public record ConstraintName(String value) {
    public ConstraintName {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("Constraint name cannot be null or blank");
        }
    }
}

public record PrimaryKey(
    List<ColumnName> columns,
    ConstraintName name
) {
    public PrimaryKey {
        if (columns == null || columns.isEmpty()) {
            throw new IllegalArgumentException("Primary key must have at least one column");
        }
    }

    public boolean contains(ColumnName column) {
        return columns.contains(column);
    }
}

public enum DeleteRule {
    NO_ACTION,
    CASCADE,
    SET_NULL,
    SET_DEFAULT,
    RESTRICT
}

public record ForeignKey(
    ConstraintName name,
    List<ColumnName> sourceColumns,
    TableName targetTable,
    List<ColumnName> targetColumns,
    DeleteRule deleteRule,
    DeleteRule updateRule
) {
    public ForeignKey {
        if (sourceColumns == null || sourceColumns.isEmpty()) {
            throw new IllegalArgumentException("Foreign key must have source columns");
        }
        if (targetTable == null) {
            throw new IllegalArgumentException("Foreign key must have target table");
        }
        if (deleteRule == null) {
            throw new IllegalArgumentException("Delete rule is required");
        }
    }
}
