package com.oracleai.workspace.schema.domain.valueobject;

public record SchemaVersion(int major, int minor) implements Comparable<SchemaVersion> {
    
    public SchemaVersion {
        if (major < 0 || minor < 0) {
            throw new IllegalArgumentException("Version numbers must be non-negative");
        }
    }

    public SchemaVersion increment() {
        return new SchemaVersion(major + 1, 0);
    }

    public SchemaVersion incrementMinor() {
        return new SchemaVersion(major, minor + 1);
    }

    @Override
    public int compareTo(SchemaVersion other) {
        int majorCompare = Integer.compare(this.major, other.major);
        if (majorCompare != 0) return majorCompare;
        return Integer.compare(this.minor, other.minor);
    }

    @Override
    public String toString() {
        return major + "." + minor;
    }
}
