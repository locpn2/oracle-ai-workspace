package com.oracleai.workspace.vector.domain.repository;

import com.oracleai.workspace.vector.domain.entity.EmbeddingJob;
import com.oracleai.workspace.vector.domain.valueobject.JobId;
import com.oracleai.workspace.vector.domain.valueobject.SearchResult;
import com.oracleai.workspace.vector.domain.valueobject.VectorEntry;

import java.util.List;
import java.util.Optional;

public interface VectorRepository {
    void saveVector(VectorEntry entry);
    void saveVectors(List<VectorEntry> entries);
    List<SearchResult> search(String query, int limit);
    List<VectorEntry> findByTableName(String tableName);
    Optional<EmbeddingJob> findJobById(JobId id);
    void saveJob(EmbeddingJob job);
    void deleteByTableName(String tableName);
    long countByTableName(String tableName);
}
