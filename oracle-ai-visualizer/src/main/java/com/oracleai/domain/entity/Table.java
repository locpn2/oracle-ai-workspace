package com.oracleai.domain.entity;

import java.util.List;
import java.util.UUID;

public class Table {
    private String id;
    private String name;
    private String comment;
    private List<Column> columns;
    private List<String> primaryKeyColumns;

    public Table(String name) {
        this.id = UUID.randomUUID().toString();
        this.name = name;
    }

    public Table(String name, List<Column> columns, List<String> primaryKeyColumns) {
        this.id = UUID.randomUUID().toString();
        this.name = name;
        this.columns = columns;
        this.primaryKeyColumns = primaryKeyColumns;
    }

    public String getId() { return id; }
    public String getName() { return name; }
    public String getComment() { return comment; }
    public List<Column> getColumns() { return columns; }
    public List<String> getPrimaryKeyColumns() { return primaryKeyColumns; }

    public void setComment(String comment) { this.comment = comment; }
    public void setColumns(List<Column> columns) { this.columns = columns; }
    public void setPrimaryKeyColumns(List<String> primaryKeyColumns) { this.primaryKeyColumns = primaryKeyColumns; }
}
