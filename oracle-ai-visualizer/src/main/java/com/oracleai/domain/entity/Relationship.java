package com.oracleai.domain.entity;

public class Relationship {
    private String id;
    private String sourceTable;
    private String sourceColumn;
    private String targetTable;
    private String targetColumn;
    private String name;

    public Relationship(String sourceTable, String sourceColumn, 
                       String targetTable, String targetColumn) {
        this.id = sourceTable + "_" + sourceColumn + "_" + targetTable;
        this.sourceTable = sourceTable;
        this.sourceColumn = sourceColumn;
        this.targetTable = targetTable;
        this.targetColumn = targetColumn;
        this.name = "FK_" + id;
    }

    public String getId() { return id; }
    public String getSourceTable() { return sourceTable; }
    public String getSourceColumn() { return sourceColumn; }
    public String getTargetTable() { return targetTable; }
    public String getTargetColumn() { return targetColumn; }
    public String getName() { return name; }
}
