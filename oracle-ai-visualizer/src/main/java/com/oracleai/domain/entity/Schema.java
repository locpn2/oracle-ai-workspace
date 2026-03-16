package com.oracleai.domain.entity;

import com.oracleai.domain.valueobject.*;
import java.util.List;
import java.util.UUID;

public class Schema {
    private SchemaId id;
    private ConnectionId connectionId;
    private String name;
    private List<Table> tables;
    private List<Relationship> relationships;
    private ExtractedAt extractedAt;

    private Schema() {}

    public Schema(SchemaId id, ConnectionId connectionId, String name) {
        this.id = id;
        this.connectionId = connectionId;
        this.name = name;
        this.extractedAt = ExtractedAt.now();
    }

    public static Schema create(ConnectionId connectionId, String name) {
        return new Schema(SchemaId.generate(), connectionId, name);
    }

    public void setTables(List<Table> tables) {
        this.tables = tables;
    }

    public void setRelationships(List<Relationship> relationships) {
        this.relationships = relationships;
    }

    public Table findTable(String tableName) {
        return tables.stream()
            .filter(t -> t.getName().equalsIgnoreCase(tableName))
            .findFirst()
            .orElseThrow(() -> new TableNotFoundException(tableName));
    }

    public SchemaId getId() { return id; }
    public ConnectionId getConnectionId() { return connectionId; }
    public String getName() { return name; }
    public List<Table> getTables() { return tables; }
    public List<Relationship> getRelationships() { return relationships; }
    public ExtractedAt getExtractedAt() { return extractedAt; }

    public record SchemaId(UUID value) {
        public static SchemaId generate() { return new SchemaId(UUID.randomUUID()); }
    }

    public record ExtractedAt(java.time.Instant value) {
        public static ExtractedAt now() { return new ExtractedAt(java.time.Instant.now()); }
    }

    public static class TableNotFoundException extends RuntimeException {
        public TableNotFoundException(String tableName) {
            super("Table not found: " + tableName);
        }
    }
}
