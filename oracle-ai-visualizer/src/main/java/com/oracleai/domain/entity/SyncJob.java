package com.oracleai.domain.entity;

import com.oracleai.domain.valueobject.*;
import java.util.List;
import java.util.UUID;

public class SyncJob {
    private JobId id;
    private UserId userId;
    private ConnectionId connectionId;
    private SyncConfig config;
    private SyncStatus status;
    private int processedRecords;
    private int totalRecords;
    private String errorMessage;
    private StartedAt startedAt;
    private CompletedAt completedAt;

    private SyncJob() {}

    public SyncJob(JobId id, UserId userId, ConnectionId connectionId, 
                   SyncConfig config, StartedAt startedAt) {
        this.id = id;
        this.userId = userId;
        this.connectionId = connectionId;
        this.config = config;
        this.status = SyncStatus.PENDING;
        this.startedAt = startedAt;
    }

    public static SyncJob create(UserId userId, ConnectionId connectionId, SyncConfig config) {
        return new SyncJob(
            JobId.generate(),
            userId,
            connectionId,
            config,
            StartedAt.now()
        );
    }

    public void start() {
        this.status = SyncStatus.RUNNING;
    }

    public void updateProgress(int processed, int total) {
        this.processedRecords = processed;
        this.totalRecords = total;
    }

    public void complete() {
        this.status = SyncStatus.COMPLETED;
        this.completedAt = CompletedAt.now();
    }

    public void fail(String error) {
        this.status = SyncStatus.FAILED;
        this.errorMessage = error;
        this.completedAt = CompletedAt.now();
    }

    public JobId getId() { return id; }
    public UserId getUserId() { return userId; }
    public ConnectionId getConnectionId() { return connectionId; }
    public SyncConfig getConfig() { return config; }
    public SyncStatus getStatus() { return status; }
    public int getProcessedRecords() { return processedRecords; }
    public int getTotalRecords() { return totalRecords; }
    public String getErrorMessage() { return errorMessage; }
    public StartedAt getStartedAt() { return startedAt; }
    public CompletedAt getCompletedAt() { return completedAt; }

    public record JobId(UUID value) {
        public static JobId generate() { return new JobId(UUID.randomUUID()); }
    }

    public record StartedAt(java.time.Instant value) {
        public static StartedAt now() { return new StartedAt(java.time.Instant.now()); }
    }

    public record CompletedAt(java.time.Instant value) {
        public static CompletedAt now() { return new CompletedAt(java.time.Instant.now()); }
    }

    public record SyncConfig(
        List<String> tableNames,
        List<ColumnMapping> columnMappings,
        String collectionName,
        boolean fullSync
    ) {
        public record ColumnMapping(String sourceColumn, String textTemplate) {}
    }

    public enum SyncStatus {
        PENDING,
        RUNNING,
        COMPLETED,
        FAILED
    }
}
