package com.oracleai.workspace.schema.application.port.out;

import com.oracleai.workspace.schema.domain.entity.SchemaMetadata;
import com.oracleai.workspace.schema.domain.entity.SchemaMetadata.SchemaId;
import com.oracleai.workspace.schema.domain.entity.SchemaMetadata.UserId;
import java.util.Optional;

public interface SchemaRepository {
    SchemaMetadata extractFromOracle(UserId userId);
    Optional<SchemaMetadata> findById(SchemaId id);
    Optional<SchemaMetadata> findByOwnerId(UserId ownerId);
    void save(SchemaMetadata schema);
    void delete(SchemaId id);
}
