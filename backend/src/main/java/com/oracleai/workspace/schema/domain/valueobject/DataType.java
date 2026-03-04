package com.oracleai.workspace.schema.domain.valueobject;

public enum DataType {
    VARCHAR2,
    NUMBER,
    INTEGER,
    FLOAT,
    DOUBLE,
    DATE,
    TIMESTAMP,
    BLOB,
    CLOB,
    CHAR,
    RAW,
    ROWID,
    XMLTYPE;

    public static DataType fromOracleType(String oracleType) {
        if (oracleType == null) {
            return VARCHAR2;
        }
        String upper = oracleType.toUpperCase();
        if (upper.contains("VARCHAR")) return VARCHAR2;
        if (upper.contains("NUMBER")) return NUMBER;
        if (upper.equals("INTEGER") || upper.equals("INT")) return INTEGER;
        if (upper.equals("FLOAT")) return FLOAT;
        if (upper.equals("DOUBLE")) return DOUBLE;
        if (upper.contains("DATE") && !upper.contains("TIMESTAMP")) return DATE;
        if (upper.contains("TIMESTAMP")) return TIMESTAMP;
        if (upper.contains("BLOB")) return BLOB;
        if (upper.contains("CLOB")) return CLOB;
        if (upper.contains("CHAR")) return CHAR;
        if (upper.contains("RAW")) return RAW;
        if (upper.equals("ROWID")) return ROWID;
        if (upper.contains("XML")) return XMLTYPE;
        return VARCHAR2;
    }

    public boolean isNumeric() {
        return this == NUMBER || this == INTEGER || this == FLOAT || this == DOUBLE;
    }

    public boolean isString() {
        return this == VARCHAR2 || this == CHAR || this == CLOB;
    }

    public boolean isDateTime() {
        return this == DATE || this == TIMESTAMP;
    }
}
