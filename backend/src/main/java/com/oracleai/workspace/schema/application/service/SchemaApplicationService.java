package com.oracleai.workspace.schema.application.service;

import com.oracleai.workspace.schema.domain.entity.SchemaMetadata;
import com.oracleai.workspace.schema.domain.entity.SchemaMetadata.UserId;
import com.oracleai.workspace.schema.application.port.in.ExtractSchemaUseCase;
import com.oracleai.workspace.schema.application.port.out.SchemaRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.Optional;

public class SchemaApplicationService implements ExtractSchemaUseCase {
    private static final Logger log = LoggerFactory.getLogger(SchemaApplicationService.class);
    
    private final SchemaRepository schemaRepository;
    
    public SchemaApplicationService(SchemaRepository schemaRepository) {
        this.schemaRepository = schemaRepository;
    }

    @Override
    public SchemaMetadata extractSchema(UserId userId) {
        log.info("Extracting schema for user: {}", userId.value());
        
        SchemaMetadata schema = schemaRepository.extractFromOracle(userId);
        
        schemaRepository.save(schema);
        
        log.info("Schema extracted successfully: {} tables", schema.getTableCount());
        
        return schema;
    }

    @Override
    public Optional<SchemaMetadata> getSchema(UserId userId) {
        return schemaRepository.findByOwnerId(userId);
    }

    @Override
    public SchemaMetadata refreshSchema(UserId userId) {
        log.info("Refreshing schema for user: {}", userId.value());
        
        SchemaMetadata schema = schemaRepository.extractFromOracle(userId);
        
        schemaRepository.save(schema);
        
        return schema;
    }
}
