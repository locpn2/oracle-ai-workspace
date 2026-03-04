package com.oracleai.workspace.schema.domain.valueobject;

import java.util.List;

public record Column(
    ColumnName name,
    DataType dataType,
    boolean nullable,
    int position,
    String defaultValue
) {
    public Column {
        if (name == null || dataType == null) {
            throw new IllegalArgumentException("Column name and data type are required");
        }
    }

    public boolean isNumeric() {
        return dataType.isNumeric();
    }

    public boolean isString() {
        return dataType.isString();
    }

    public boolean isDateTime() {
        return dataType.isDateTime();
    }
}
