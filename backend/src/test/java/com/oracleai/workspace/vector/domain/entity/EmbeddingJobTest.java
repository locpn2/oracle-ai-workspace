package com.oracleai.workspace.vector.domain.entity;

import com.oracleai.workspace.vector.domain.valueobject.*;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

class EmbeddingJobTest {

    @Test
    void createJob_WithValidData_ReturnsJob() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();

        assertNotNull(job);
        assertEquals(1000, job.getTotalRows());
        assertEquals(JobStatus.PENDING, job.getStatus());
        assertEquals(0, job.getProcessedRows());
    }

    @Test
    void createJob_WithoutUserId_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () ->
                EmbeddingJob.builder()
                        .sourceTable(new EmbeddingJob.TableName("USERS"))
                        .totalRows(1000)
                        .build()
        );
    }

    @Test
    void createJob_WithoutSourceTable_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () ->
                EmbeddingJob.builder()
                        .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                        .totalRows(1000)
                        .build()
        );
    }

    @Test
    void createJob_WithZeroTotalRows_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () ->
                EmbeddingJob.builder()
                        .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                        .sourceTable(new EmbeddingJob.TableName("USERS"))
                        .totalRows(0)
                        .build()
        );
    }

    @Test
    void start_ChangesStatusToProcessing() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();

        job.start();

        assertEquals(JobStatus.PROCESSING, job.getStatus());
    }

    @Test
    void start_WithNonPendingStatus_ThrowsException() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();
        
        job.start(); // Now status is PROCESSING
        
        assertThrows(IllegalStateException.class, () -> job.start());
    }

    @Test
    void completeBatch_IncrementsProcessedRows() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();
        
        job.start();
        job.completeBatch(100);

        assertEquals(100, job.getProcessedRows());
    }

    @Test
    void completeBatch_WhenAllRowsProcessed_ChangesStatusToCompleted() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(100)
                .build();
        
        job.start();
        job.completeBatch(100);

        assertEquals(JobStatus.COMPLETED, job.getStatus());
        assertTrue(job.getCompletedAt().isPresent());
    }

    @Test
    void fail_ChangesStatusToFailed() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();
        
        job.start();
        job.fail(EmbeddingJob.ErrorReason.of("ERROR_CODE", "Error message"));

        assertEquals(JobStatus.FAILED, job.getStatus());
        assertTrue(job.getFailureReason().isPresent());
        assertEquals("ERROR_CODE", job.getFailureReason().get().code());
    }

    @Test
    void fail_WithoutReason_ThrowsException() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();

        assertThrows(IllegalArgumentException.class, () -> job.fail(null));
    }

    @Test
    void retry_ResetsJobForRetry() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();
        
        job.start();
        job.fail(EmbeddingJob.ErrorReason.of("ERROR_CODE", "Error"));
        
        job.retry();

        assertEquals(JobStatus.PENDING, job.getStatus());
        assertEquals(0, job.getProcessedRows());
        assertTrue(job.getFailureReason().isEmpty());
    }

    @Test
    void retry_WithNonFailedStatus_ThrowsException() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();
        
        job.start();
        job.completeBatch(100);

        assertThrows(IllegalStateException.class, () -> job.retry());
    }

    @Test
    void cancel_ChangesStatusToCancelled() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();
        
        job.start();
        job.cancel();

        assertEquals(JobStatus.CANCELLED, job.getStatus());
    }

    @Test
    void cancel_WithCompletedStatus_ThrowsException() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();
        
        job.start();
        job.completeBatch(1000);

        assertThrows(IllegalStateException.class, () -> job.cancel());
    }

    @Test
    void getProgress_ReturnsCorrectPercentage() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(1000)
                .build();
        
        job.start();
        job.completeBatch(250);

        assertEquals(0.25, job.getProgress(), 0.001);
    }

    @Test
    void getProgress_WithZeroTotalRows_ReturnsZero() {
        EmbeddingJob job = EmbeddingJob.builder()
                .userId(new EmbeddingJob.UserId(UUID.randomUUID()))
                .sourceTable(new EmbeddingJob.TableName("USERS"))
                .totalRows(100)
                .build();

        assertEquals(0.0, job.getProgress(), 0.001);
    }
}
