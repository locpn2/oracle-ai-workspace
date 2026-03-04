package com.oracleai.workspace.vector.domain.entity;

import com.oracleai.workspace.vector.domain.valueobject.*;
import java.time.Instant;
import java.util.*;

public final class EmbeddingJob {
    private final JobId id;
    private final UserId userId;
    private final TableName sourceTable;
    private JobStatus status;
    private final long totalRows;
    private long processedRows;
    private final List<EmbeddingBatch> batches;
    private final EmbeddingConfig config;
    private final Instant createdAt;
    private Instant completedAt;
    private ErrorReason failureReason;

    private EmbeddingJob(Builder builder) {
        this.id = builder.id;
        this.userId = builder.userId;
        this.sourceTable = builder.sourceTable;
        this.status = builder.status;
        this.totalRows = builder.totalRows;
        this.processedRows = 0;
        this.batches = new ArrayList<>(builder.batches);
        this.config = builder.config;
        this.createdAt = builder.createdAt;
    }

    public JobId getId() {
        return id;
    }

    public UserId getUserId() {
        return userId;
    }

    public TableName getSourceTable() {
        return sourceTable;
    }

    public JobStatus getStatus() {
        return status;
    }

    public long getTotalRows() {
        return totalRows;
    }

    public long getProcessedRows() {
        return processedRows;
    }

    public List<EmbeddingBatch> getBatches() {
        return List.copyOf(batches);
    }

    public EmbeddingConfig getConfig() {
        return config;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public Optional<Instant> getCompletedAt() {
        return Optional.ofNullable(completedAt);
    }

    public Optional<ErrorReason> getFailureReason() {
        return Optional.ofNullable(failureReason);
    }

    public double getProgress() {
        if (totalRows == 0) return 0.0;
        return (double) processedRows / totalRows;
    }

    public void start() {
        if (status != JobStatus.PENDING) {
            throw new IllegalStateException(
                "Cannot start job in status: " + status + ". Only PENDING jobs can be started.");
        }
        this.status = JobStatus.PROCESSING;
    }

    public void completeBatch(int rowCount) {
        if (status != JobStatus.PROCESSING) {
            throw new IllegalStateException("Job not processing");
        }
        this.processedRows += rowCount;

        if (this.processedRows >= this.totalRows) {
            this.status = JobStatus.COMPLETED;
            this.completedAt = Instant.now();
        }
    }

    public void fail(ErrorReason reason) {
        if (reason == null) {
            throw new IllegalArgumentException("Failure reason required");
        }
        this.status = JobStatus.FAILED;
        this.failureReason = reason;
    }

    public void retry() {
        if (status != JobStatus.FAILED && status != JobStatus.CANCELLED) {
            throw new IllegalStateException("Can only retry FAILED or CANCELLED jobs");
        }
        this.status = JobStatus.PENDING;
        this.processedRows = 0;
        this.failureReason = null;
    }

    public void cancel() {
        if (status == JobStatus.COMPLETED) {
            throw new IllegalStateException("Cannot cancel completed job");
        }
        this.status = JobStatus.CANCELLED;
    }

    public record JobId(UUID value) {
        public JobId {
            if (value == null) {
                throw new IllegalArgumentException("Job ID cannot be null");
            }
        }

        public static JobId generate() {
            return new JobId(UUID.randomUUID());
        }
    }

    public record UserId(UUID value) {
        public UserId {
            if (value == null) {
                throw new IllegalArgumentException("User ID cannot be null");
            }
        }
    }

    public record TableName(String value) {
        public TableName {
            if (value == null || value.isBlank()) {
                throw new IllegalArgumentException("Table name cannot be null or blank");
            }
        }
    }

    public record ErrorReason(String code, String message, Throwable cause) {
        public static ErrorReason of(String code, String message) {
            return new ErrorReason(code, message, null);
        }
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private JobId id = JobId.generate();
        private UserId userId;
        private TableName sourceTable;
        private JobStatus status = JobStatus.PENDING;
        private long totalRows;
        private List<EmbeddingBatch> batches = new ArrayList<>();
        private EmbeddingConfig config = EmbeddingConfig.defaultConfig();
        private Instant createdAt = Instant.now();

        public Builder id(JobId id) {
            this.id = id;
            return this;
        }

        public Builder userId(UserId userId) {
            this.userId = userId;
            return this;
        }

        public Builder sourceTable(TableName sourceTable) {
            this.sourceTable = sourceTable;
            return this;
        }

        public Builder totalRows(long totalRows) {
            this.totalRows = totalRows;
            return this;
        }

        public Builder config(EmbeddingConfig config) {
            this.config = config;
            return this;
        }

        public EmbeddingJob build() {
            if (userId == null) {
                throw new IllegalArgumentException("User ID is required");
            }
            if (sourceTable == null) {
                throw new IllegalArgumentException("Source table is required");
            }
            if (totalRows <= 0) {
                throw new IllegalArgumentException("Total rows must be positive");
            }
            return new EmbeddingJob(this);
        }
    }
}
