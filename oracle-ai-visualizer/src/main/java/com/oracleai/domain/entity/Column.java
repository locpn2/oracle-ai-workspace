package com.oracleai.domain.entity;

public class Column {
    private String name;
    private String dataType;
    private boolean nullable;
    private String defaultValue;
    private String comment;

    public Column(String name, String dataType, boolean nullable) {
        this.name = name;
        this.dataType = dataType;
        this.nullable = nullable;
    }

    public String getName() { return name; }
    public String getDataType() { return dataType; }
    public boolean isNullable() { return nullable; }
    public String getDefaultValue() { return defaultValue; }
    public String getComment() { return comment; }

    public void setDefaultValue(String defaultValue) { this.defaultValue = defaultValue; }
    public void setComment(String comment) { this.comment = comment; }
}
