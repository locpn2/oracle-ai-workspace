package com.oracleai.workspace.schema.application.port.in;

import com.oracleai.workspace.schema.domain.entity.SchemaMetadata;
import com.oracleai.workspace.schema.domain.entity.SchemaMetadata.UserId;
import java.util.Optional;

public interface ExtractSchemaUseCase {
    SchemaMetadata extractSchema(UserId userId);
    Optional<SchemaMetadata> getSchema(UserId userId);
    SchemaMetadata refreshSchema(UserId userId);
}
