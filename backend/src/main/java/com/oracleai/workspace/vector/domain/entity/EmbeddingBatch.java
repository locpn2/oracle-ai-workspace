package com.oracleai.workspace.vector.domain.entity;

import com.oracleai.workspace.vector.domain.valueobject.*;
import java.util.List;

public final class EmbeddingBatch {
    private final BatchId id;
    private final int batchNumber;
    private final long startRow;
    private final long endRow;
    private BatchStatus status;
    private List<VectorEntry> vectors;

    private EmbeddingBatch(Builder builder) {
        this.id = builder.id;
        this.batchNumber = builder.batchNumber;
        this.startRow = builder.startRow;
        this.endRow = builder.endRow;
        this.status = builder.status;
    }

    public BatchId getId() {
        return id;
    }

    public int getBatchNumber() {
        return batchNumber;
    }

    public long getStartRow() {
        return startRow;
    }

    public long getEndRow() {
        return endRow;
    }

    public BatchStatus getStatus() {
        return status;
    }

    public List<VectorEntry> getVectors() {
        return vectors;
    }

    public boolean isComplete() {
        return status == BatchStatus.COMPLETED;
    }

    public void setVectors(List<VectorEntry> vectors) {
        this.vectors = vectors;
        this.status = BatchStatus.COMPLETED;
    }

    public void fail() {
        this.status = BatchStatus.FAILED;
    }

    public record BatchId(java.util.UUID value) {
        public BatchId {
            if (value == null) {
                throw new IllegalArgumentException("Batch ID cannot be null");
            }
        }

        public static BatchId generate() {
            return new BatchId(java.util.UUID.randomUUID());
        }
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private BatchId id = BatchId.generate();
        private int batchNumber;
        private long startRow;
        private long endRow;
        private BatchStatus status = BatchStatus.QUEUED;

        public Builder id(BatchId id) {
            this.id = id;
            return this;
        }

        public Builder batchNumber(int batchNumber) {
            this.batchNumber = batchNumber;
            return this;
        }

        public Builder startRow(long startRow) {
            this.startRow = startRow;
            return this;
        }

        public Builder endRow(long endRow) {
            this.endRow = endRow;
            return this;
        }

        public Builder status(BatchStatus status) {
            this.status = status;
            return this;
        }

        public EmbeddingBatch build() {
            if (startRow < 0 || endRow <= startRow) {
                throw new IllegalArgumentException("Invalid row range");
            }
            return new EmbeddingBatch(this);
        }
    }
}
