package com.oracleai.workspace.schema.application.service;

import com.oracleai.workspace.schema.application.dto.ColumnDTO;
import com.oracleai.workspace.schema.application.dto.ERDResponse;
import com.oracleai.workspace.schema.application.dto.TableDTO;
import com.oracleai.workspace.schema.domain.entity.Table;
import com.oracleai.workspace.schema.domain.repository.TableRepository;
import com.oracleai.workspace.schema.domain.valueobject.ColumnName;
import com.oracleai.workspace.schema.domain.valueobject.PrimaryKey;
import com.oracleai.workspace.schema.domain.valueobject.TableName;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class TableMetadataService {

    private static final Logger log = LoggerFactory.getLogger(TableMetadataService.class);

    private final TableRepository tableRepository;

    public TableMetadataService(TableRepository tableRepository) {
        this.tableRepository = tableRepository;
    }

    public List<TableDTO> getAllTables() {
        log.info("Fetching all tables");
        return tableRepository.findAll().stream()
                .map(this::toTableDTO)
                .collect(Collectors.toList());
    }

    public TableDTO getTableByName(String name) {
        log.info("Fetching table: {}", name);
        TableName tableName = new TableName(name);
        return tableRepository.findByName(tableName)
                .map(this::toTableDTO)
                .orElse(null);
    }

    public List<ColumnDTO> getColumnsForTable(String tableName) {
        log.info("Fetching columns for table: {}", tableName);
        TableName name = new TableName(tableName);
        return tableRepository.findByName(name)
                .map(table -> table.getColumns().stream()
                        .map(col -> new ColumnDTO(
                                col.name().value(),
                                col.dataType().name(),
                                col.nullable(),
                                col.position(),
                                col.defaultValue()
                        ))
                        .collect(Collectors.toList()))
                .orElse(List.of());
    }

    public ERDResponse getERD() {
        log.info("Generating ERD");
        List<Table> tables = tableRepository.findAll();
        
        List<TableDTO> tableDTOs = tables.stream()
                .map(this::toTableDTO)
                .collect(Collectors.toList());
        
        List<ERDResponse.RelationshipDTO> relationships = tables.stream()
                .flatMap(table -> table.getForeignKeys().stream()
                        .map(fk -> new ERDResponse.RelationshipDTO(
                                table.getName().value(),
                                fk.targetTable().value(),
                                fk.sourceColumns().stream().map(ColumnName::value).collect(Collectors.toList()),
                                fk.targetColumns().stream().map(ColumnName::value).collect(Collectors.toList())
                        )))
                .collect(Collectors.toList());
        
        Map<String, Object> metadata = Map.of(
                "tableCount", tables.size(),
                "relationshipCount", relationships.size()
        );
        
        return new ERDResponse(tableDTOs, relationships, metadata);
    }

    private TableDTO toTableDTO(Table table) {
        TableDTO.PrimaryKeyDTO pkDTO = null;
        if (table.getPrimaryKey().isPresent()) {
            PrimaryKey pk = table.getPrimaryKey().get();
            pkDTO = new TableDTO.PrimaryKeyDTO(
                    pk.name().value(),
                    pk.columns().stream()
                            .map(ColumnName::value)
                            .collect(Collectors.toList())
            );
        }
        
        List<TableDTO.ForeignKeyDTO> fkDTOs = table.getForeignKeys().stream()
                .map(fk -> new TableDTO.ForeignKeyDTO(
                        fk.name().value(),
                        fk.sourceColumns().stream().map(ColumnName::value).collect(Collectors.toList()),
                        fk.targetTable().value(),
                        fk.targetColumns().stream().map(ColumnName::value).collect(Collectors.toList()),
                        fk.deleteRule().name()
                ))
                .collect(Collectors.toList());
        
        return new TableDTO(
                table.getName().value(),
                table.getType().name(),
                table.getColumns().stream()
                        .map(col -> new ColumnDTO(
                                col.name().value(),
                                col.dataType().name(),
                                col.nullable(),
                                col.position(),
                                col.defaultValue()
                        ))
                        .collect(Collectors.toList()),
                pkDTO,
                fkDTOs
        );
    }
}
