package com.oracleai.workspace.schema.domain.valueobject;

import java.util.ArrayList;
import java.util.List;

public final class ForeignKey {
    private final ConstraintName name;
    private final List<ColumnName> sourceColumns;
    private final TableName targetTable;
    private final List<ColumnName> targetColumns;
    private final DeleteRule deleteRule;

    private ForeignKey(Builder builder) {
        this.name = builder.name;
        this.sourceColumns = List.copyOf(builder.sourceColumns);
        this.targetTable = builder.targetTable;
        this.targetColumns = List.copyOf(builder.targetColumns);
        this.deleteRule = builder.deleteRule;
    }

    public ConstraintName name() { return name; }
    public List<ColumnName> sourceColumns() { return sourceColumns; }
    public TableName targetTable() { return targetTable; }
    public List<ColumnName> targetColumns() { return targetColumns; }
    public DeleteRule deleteRule() { return deleteRule; }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private ConstraintName name;
        private List<ColumnName> sourceColumns = new ArrayList<>();
        private TableName targetTable;
        private List<ColumnName> targetColumns = new ArrayList<>();
        private DeleteRule deleteRule = DeleteRule.NO_ACTION;

        public Builder name(ConstraintName name) {
            this.name = name;
            return this;
        }

        public Builder addSourceColumn(ColumnName column) {
            this.sourceColumns.add(column);
            return this;
        }

        public Builder sourceColumns(List<ColumnName> sourceColumns) {
            this.sourceColumns = sourceColumns;
            return this;
        }

        public Builder targetTable(TableName targetTable) {
            this.targetTable = targetTable;
            return this;
        }

        public Builder addTargetColumn(ColumnName column) {
            this.targetColumns.add(column);
            return this;
        }

        public Builder targetColumns(List<ColumnName> targetColumns) {
            this.targetColumns = targetColumns;
            return this;
        }

        public Builder deleteRule(DeleteRule deleteRule) {
            this.deleteRule = deleteRule;
            return this;
        }

        public ForeignKey build() {
            if (name == null) {
                throw new IllegalArgumentException("Foreign key name is required");
            }
            if (sourceColumns.isEmpty()) {
                throw new IllegalArgumentException("Foreign key must have source columns");
            }
            if (targetTable == null) {
                throw new IllegalArgumentException("Foreign key must have target table");
            }
            return new ForeignKey(this);
        }
    }
}
