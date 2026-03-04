package com.oracleai.workspace.schema.domain.entity;

import com.oracleai.workspace.schema.domain.valueobject.*;
import java.time.Instant;
import java.util.*;

public final class SchemaMetadata {
    private final SchemaId id;
    private final UserId ownerId;
    private final List<Table> tables;
    private final Instant extractedAt;
    private final SchemaVersion version;

    private SchemaMetadata(Builder builder) {
        this.id = builder.id;
        this.ownerId = builder.ownerId;
        this.tables = List.copyOf(builder.tables);
        this.extractedAt = builder.extractedAt;
        this.version = builder.version;
    }

    public SchemaId getId() {
        return id;
    }

    public UserId getOwnerId() {
        return ownerId;
    }

    public List<Table> getTables() {
        return tables;
    }

    public Instant getExtractedAt() {
        return extractedAt;
    }

    public SchemaVersion getVersion() {
        return version;
    }

    public Optional<Table> getTable(TableName name) {
        return tables.stream()
            .filter(t -> t.getName().equals(name))
            .findFirst();
    }

    public boolean hasTable(TableName name) {
        return getTable(name).isPresent();
    }

    public int getTableCount() {
        return tables.size();
    }

    public int getTotalColumnCount() {
        return tables.stream()
            .mapToInt(t -> t.getColumns().size())
            .sum();
    }

    public List<ForeignKey> getAllForeignKeys() {
        return tables.stream()
            .flatMap(t -> t.getForeignKeys().stream())
            .toList();
    }

    public List<Table> getTablesReferencing(TableName targetTable) {
        return tables.stream()
            .filter(t -> t.getForeignKeys().stream()
                .anyMatch(fk -> fk.targetTable().equals(targetTable)))
            .toList();
    }

    public SchemaMetadata withTables(List<Table> newTables) {
        return Builder.builder()
            .id(this.id)
            .ownerId(this.ownerId)
            .tables(newTables)
            .extractedAt(this.extractedAt)
            .version(this.version)
            .build();
    }

    public record SchemaId(UUID value) {
        public SchemaId {
            if (value == null) {
                throw new IllegalArgumentException("Schema ID cannot be null");
            }
        }

        public static SchemaId generate() {
            return new SchemaId(UUID.randomUUID());
        }
    }

    public record UserId(UUID value) {
        public UserId {
            if (value == null) {
                throw new IllegalArgumentException("User ID cannot be null");
            }
        }
    }

    public record SchemaVersion(int major, int minor) implements Comparable<SchemaVersion> {
        public SchemaMetadata increment() {
            return Builder.builder()
                .id(SchemaId.generate())
                .ownerId(this.ownerId)
                .tables(this.tables)
                .extractedAt(Instant.now())
                .version(new SchemaVersion(major + 1, 0))
                .build();
        }

        @Override
        public int compareTo(SchemaVersion other) {
            int cmp = Integer.compare(this.major, other.major);
            return cmp != 0 ? cmp : Integer.compare(this.minor, other.minor);
        }
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private SchemaId id = SchemaId.generate();
        private UserId ownerId;
        private List<Table> tables = new ArrayList<>();
        private Instant extractedAt = Instant.now();
        private SchemaVersion version = new SchemaVersion(1, 0);

        public Builder id(SchemaId id) {
            this.id = id;
            return this;
        }

        public Builder ownerId(UserId ownerId) {
            this.ownerId = ownerId;
            return this;
        }

        public Builder tables(List<Table> tables) {
            this.tables = tables;
            return this;
        }

        public Builder addTable(Table table) {
            this.tables.add(table);
            return this;
        }

        public Builder extractedAt(Instant extractedAt) {
            this.extractedAt = extractedAt;
            return this;
        }

        public Builder version(SchemaVersion version) {
            this.version = version;
            return this;
        }

        public SchemaMetadata build() {
            if (ownerId == null) {
                throw new IllegalArgumentException("Owner ID is required");
            }
            if (tables.isEmpty()) {
                throw new IllegalArgumentException("Schema must have at least one table");
            }
            return new SchemaMetadata(this);
        }
    }
}
