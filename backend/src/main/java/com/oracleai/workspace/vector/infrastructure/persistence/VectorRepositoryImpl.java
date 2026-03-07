package com.oracleai.workspace.vector.infrastructure.persistence;

import com.oracleai.workspace.vector.domain.entity.EmbeddingJob;
import com.oracleai.workspace.vector.domain.repository.VectorRepository;
import com.oracleai.workspace.vector.domain.valueobject.JobId;
import com.oracleai.workspace.vector.domain.valueobject.SearchResult;
import com.oracleai.workspace.vector.domain.valueobject.VectorEntry;
import jakarta.persistence.*;
import org.hibernate.Session;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.util.*;

@Repository
public class VectorRepositoryImpl implements VectorRepository {

    private static final Logger log = LoggerFactory.getLogger(VectorRepositoryImpl.class);

    private final EntityManager entityManager;

    public VectorRepositoryImpl(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    @Override
    public void saveVector(VectorEntry entry) {
        log.debug("Saving vector for row: {}", entry.rowId().value());
        
        VectorEntity entity = new VectorEntity();
        entity.setRowId(entry.rowId().value());
        entity.setDocument(entry.document());
        entity.setEmbedding(entry.embedding());
        
        entityManager.persist(entity);
    }

    @Override
    public void saveVectors(List<VectorEntry> entries) {
        log.info("Saving {} vectors in batch", entries.size());
        
        for (int i = 0; i < entries.size(); i++) {
            VectorEntry entry = entries.get(i);
            VectorEntity entity = new VectorEntity();
            entity.setRowId(entry.rowId().value());
            entity.setDocument(entry.document());
            entity.setEmbedding(entry.embedding());
            
            entityManager.persist(entity);
            
            if (i % 50 == 0) {
                entityManager.flush();
                entityManager.clear();
            }
        }
    }

    @Override
    @SuppressWarnings("unchecked")
    public List<SearchResult> search(String query, int limit) {
        log.debug("Searching for: {} with limit: {}", query, limit);
        
        String sql = """
            SELECT row_id, document, 1 - (embedding <=> CAST(:queryVector AS vector)) AS similarity
            FROM vector_entries
            ORDER BY embedding <=> CAST(:queryVector AS vector)
            LIMIT :limit
            """;
        
        List<Object[]> results = entityManager.unwrap(Session.class)
                .createNativeQuery(sql)
                .setParameter("queryVector", query.getBytes())
                .setParameter("limit", limit)
                .getResultList();
        
        return results.stream()
                .map(row -> {
                    VectorEntry entry = new VectorEntry(
                            new VectorEntry.RowId((String) row[0]),
                            (String) row[1],
                            (float[]) row[2],
                            ((Number) row[2]).doubleValue()
                    );
                    double similarity = ((Number) row[2]).doubleValue();
                    return SearchResult.of(entry, similarity);
                })
                .toList();
    }

    @Override
    @SuppressWarnings("unchecked")
    public List<VectorEntry> findByTableName(String tableName) {
        String sql = "SELECT row_id, document, embedding FROM vector_entries WHERE row_id LIKE :tableNamePattern";
        
        List<Object[]> results = entityManager.unwrap(Session.class)
                .createNativeQuery(sql)
                .setParameter("tableNamePattern", tableName + "_%")
                .getResultList();
        
        return results.stream()
                .map(row -> new VectorEntry(
                        new VectorEntry.RowId((String) row[0]),
                        (String) row[1],
                        (float[]) row[2],
                        0.0
                ))
                .toList();
    }

    @Override
    public Optional<EmbeddingJob> findJobById(JobId id) {
        EmbeddingJobEntity entity = entityManager.find(EmbeddingJobEntity.class, id.value().toString());
        
        if (entity == null) {
            return Optional.empty();
        }
        
        return Optional.of(mapToJob(entity));
    }

    @Override
    public void saveJob(EmbeddingJob job) {
        EmbeddingJobEntity entity = mapToEntity(job);
        
        if (entityManager.find(EmbeddingJobEntity.class, job.getId().value().toString()) != null) {
            entityManager.merge(entity);
        } else {
            entityManager.persist(entity);
        }
    }

    @Override
    public void deleteByTableName(String tableName) {
        log.info("Deleting vectors for table: {}", tableName);
        
        String sql = "DELETE FROM vector_entries WHERE row_id LIKE :tableNamePattern";
        entityManager.unwrap(Session.class)
                .createNativeQuery(sql)
                .setParameter("tableNamePattern", tableName + "_%")
                .executeUpdate();
    }

    @Override
    public long countByTableName(String tableName) {
        String sql = "SELECT COUNT(*) FROM vector_entries WHERE row_id LIKE :tableNamePattern";
        
        Number count = (Number) entityManager.unwrap(Session.class)
                .createNativeQuery(sql)
                .setParameter("tableNamePattern", tableName + "_%")
                .getSingleResult();
        
        return count.longValue();
    }

    private EmbeddingJob mapToJob(EmbeddingJobEntity entity) {
        EmbeddingJob.Builder builder = EmbeddingJob.builder()
                .id(new EmbeddingJob.JobId(UUID.fromString(entity.getId())))
                .userId(new EmbeddingJob.UserId(UUID.fromString(entity.getUserId())))
                .sourceTable(new EmbeddingJob.TableName(entity.getSourceTable()))
                .totalRows(entity.getTotalRows());
        
        return builder.build();
    }

    private EmbeddingJobEntity mapToEntity(EmbeddingJob job) {
        EmbeddingJobEntity entity = new EmbeddingJobEntity();
        entity.setId(job.getId().value().toString());
        entity.setUserId(job.getUserId().value().toString());
        entity.setSourceTable(job.getSourceTable().value());
        entity.setTotalRows(job.getTotalRows());
        entity.setStatus(job.getStatus().name());
        return entity;
    }

    @Entity
    @Table(name = "vector_entries")
    public static class VectorEntity {
        
        @Id
        @Column(name = "row_id")
        private String rowId;
        
        @Column(name = "document", columnDefinition = "TEXT")
        private String document;
        
        @Column(name = "embedding", columnDefinition = "vector(768)")
        private float[] embedding;

        public String getRowId() { return rowId; }
        public void setRowId(String rowId) { this.rowId = rowId; }
        
        public String getDocument() { return document; }
        public void setDocument(String document) { this.document = document; }
        
        public float[] getEmbedding() { return embedding; }
        public void setEmbedding(float[] embedding) { this.embedding = embedding; }
    }

    @Entity
    @Table(name = "embedding_jobs")
    public static class EmbeddingJobEntity {
        
        @Id
        private String id;
        
        @Column(name = "user_id")
        private String userId;
        
        @Column(name = "source_table")
        private String sourceTable;
        
        private long totalRows;
        private String status;

        public String getId() { return id; }
        public void setId(String id) { this.id = id; }
        
        public String getUserId() { return userId; }
        public void setUserId(String userId) { this.userId = userId; }
        
        public String getSourceTable() { return sourceTable; }
        public void setSourceTable(String sourceTable) { this.sourceTable = sourceTable; }
        
        public long getTotalRows() { return totalRows; }
        public void setTotalRows(long totalRows) { this.totalRows = totalRows; }
        
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
    }
}
