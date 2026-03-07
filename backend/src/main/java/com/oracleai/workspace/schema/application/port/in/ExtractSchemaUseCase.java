package com.oracleai.workspace.schema.application.port.in;

import com.oracleai.workspace.schema.domain.entity.SchemaMetadata;
import java.util.Optional;

public interface ExtractSchemaUseCase {
    SchemaMetadata extractSchema(String userId);
    Optional<SchemaMetadata> getSchema(String userId);
    SchemaMetadata refreshSchema(String userId);
}
