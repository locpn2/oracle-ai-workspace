package com.oracleai.workspace.schema.application.port.out;

import com.oracleai.workspace.schema.domain.entity.SchemaMetadata;
import com.oracleai.workspace.schema.domain.valueobject.SchemaId;
import java.util.Optional;

public interface SchemaRepository {
    SchemaMetadata extractFromOracle(String userId);
    Optional<SchemaMetadata> findById(SchemaId id);
    Optional<SchemaMetadata> findByOwnerId(String ownerId);
    void save(SchemaMetadata schema);
    void delete(SchemaId id);
}
