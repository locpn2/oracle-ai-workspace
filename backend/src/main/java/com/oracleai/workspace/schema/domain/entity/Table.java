package com.oracleai.workspace.schema.domain.entity;

import com.oracleai.workspace.schema.domain.valueobject.*;
import java.util.*;

public final class Table {
    private final TableName name;
    private final List<Column> columns;
    private final PrimaryKey primaryKey;
    private final List<ForeignKey> foreignKeys;
    private final TableType type;
    private final long rowCount;

    private Table(Builder builder) {
        this.name = builder.name;
        this.columns = List.copyOf(builder.columns);
        this.primaryKey = builder.primaryKey;
        this.foreignKeys = List.copyOf(builder.foreignKeys);
        this.type = builder.type;
        this.rowCount = builder.rowCount;
    }

    public TableName getName() {
        return name;
    }

    public List<Column> getColumns() {
        return columns;
    }

    public Optional<PrimaryKey> getPrimaryKey() {
        return Optional.ofNullable(primaryKey);
    }

    public List<ForeignKey> getForeignKeys() {
        return foreignKeys;
    }

    public TableType getType() {
        return type;
    }

    public long getRowCount() {
        return rowCount;
    }

    public boolean hasColumn(ColumnName columnName) {
        return columns.stream()
            .anyMatch(c -> c.name().equals(columnName));
    }

    public Optional<Column> findColumn(ColumnName columnName) {
        return columns.stream()
            .filter(c -> c.name().equals(columnName))
            .findFirst();
    }

    public Optional<ForeignKey> findForeignKeyTo(TableName targetTable) {
        return foreignKeys.stream()
            .filter(fk -> fk.targetTable().equals(targetTable))
            .findFirst();
    }

    public List<ColumnName> getColumnNames() {
        return columns.stream()
            .map(Column::name)
            .toList();
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private TableName name;
        private List<Column> columns = new ArrayList<>();
        private PrimaryKey primaryKey;
        private List<ForeignKey> foreignKeys = new ArrayList<>();
        private TableType type = TableType.TABLE;
        private long rowCount = 0;

        public Builder name(TableName name) {
            this.name = name;
            return this;
        }

        public Builder columns(List<Column> columns) {
            this.columns = columns;
            return this;
        }

        public Builder addColumn(Column column) {
            this.columns.add(column);
            return this;
        }

        public Builder primaryKey(PrimaryKey primaryKey) {
            this.primaryKey = primaryKey;
            return this;
        }

        public Builder foreignKeys(List<ForeignKey> foreignKeys) {
            this.foreignKeys = foreignKeys;
            return this;
        }

        public Builder type(TableType type) {
            this.type = type;
            return this;
        }

        public Builder rowCount(long rowCount) {
            this.rowCount = rowCount;
            return this;
        }

        public Table build() {
            if (name == null) {
                throw new IllegalArgumentException("Table name is required");
            }
            return new Table(this);
        }
    }
}
