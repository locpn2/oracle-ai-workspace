package com.oracleai.workspace.schema.domain.valueobject;

public enum TableType {
    TABLE,
    VIEW,
    MATERIALIZED_VIEW,
    SYNONYM;

    public static TableType fromOracleType(String oracleType) {
        if (oracleType == null) return TABLE;
        return switch (oracleType.toUpperCase()) {
            case "VIEW" -> VIEW;
            case "MATERIALIZED VIEW" -> MATERIALIZED_VIEW;
            case "SYNONYM" -> SYNONYM;
            default -> TABLE;
        };
    }
}
