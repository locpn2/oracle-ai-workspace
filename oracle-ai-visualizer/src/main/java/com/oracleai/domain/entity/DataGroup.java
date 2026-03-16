package com.oracleai.domain.entity;

import com.oracleai.domain.valueobject.*;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class DataGroup {
    private GroupId id;
    private UserId ownerId;
    private GroupName name;
    private String description;
    private List<String> tableIds;
    private CreatedAt createdAt;

    private DataGroup() {}

    public DataGroup(GroupId id, UserId ownerId, GroupName name, CreatedAt createdAt) {
        this.id = id;
        this.ownerId = ownerId;
        this.name = name;
        this.createdAt = createdAt;
        this.tableIds = new ArrayList<>();
    }

    public static DataGroup create(UserId ownerId, String name, String description) {
        return new DataGroup(
            GroupId.generate(),
            ownerId,
            new GroupName(name),
            CreatedAt.now()
        );
    }

    public void addTable(String tableId) {
        if (tableIds.contains(tableId)) {
            throw new TableAlreadyInGroupException(tableId);
        }
        tableIds.add(tableId);
    }

    public void removeTable(String tableId) {
        tableIds.remove(tableId);
    }

    public GroupId getId() { return id; }
    public UserId getOwnerId() { return ownerId; }
    public GroupName getName() { return name; }
    public String getDescription() { return description; }
    public List<String> getTableIds() { return tableIds; }
    public CreatedAt getCreatedAt() { return createdAt; }

    public void setDescription(String description) { this.description = description; }

    public record GroupId(UUID value) {
        public static GroupId generate() { return new GroupId(UUID.randomUUID()); }
    }

    public static class TableAlreadyInGroupException extends RuntimeException {
        public TableAlreadyInGroupException(String tableId) {
            super("Table already in group: " + tableId);
        }
    }
}
