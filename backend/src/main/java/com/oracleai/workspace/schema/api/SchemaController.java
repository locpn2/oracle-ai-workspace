package com.oracleai.workspace.schema.api;

import com.oracleai.workspace.schema.application.dto.ColumnDTO;
import com.oracleai.workspace.schema.application.dto.ERDResponse;
import com.oracleai.workspace.schema.application.dto.TableDTO;
import com.oracleai.workspace.schema.application.service.TableMetadataService;
import com.oracleai.workspace.shared.dto.ApiResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/schema")
public class SchemaController {

    private static final Logger log = LoggerFactory.getLogger(SchemaController.class);

    private final TableMetadataService tableMetadataService;

    public SchemaController(TableMetadataService tableMetadataService) {
        this.tableMetadataService = tableMetadataService;
    }

    @GetMapping("/tables")
    public ResponseEntity<ApiResponse<List<TableDTO>>> getAllTables() {
        log.info("GET /api/schema/tables");
        List<TableDTO> tables = tableMetadataService.getAllTables();
        return ResponseEntity.ok(ApiResponse.success(tables));
    }

    @GetMapping("/tables/{name}")
    public ResponseEntity<ApiResponse<TableDTO>> getTableByName(@PathVariable String name) {
        log.info("GET /api/schema/tables/{}", name);
        TableDTO table = tableMetadataService.getTableByName(name.toUpperCase());
        if (table == null) {
            return ResponseEntity.ok(ApiResponse.error("Table not found", "NOT_FOUND"));
        }
        return ResponseEntity.ok(ApiResponse.success(table));
    }

    @GetMapping("/columns/{table}")
    public ResponseEntity<ApiResponse<List<ColumnDTO>>> getColumns(@PathVariable String table) {
        log.info("GET /api/schema/columns/{}", table);
        List<ColumnDTO> columns = tableMetadataService.getColumnsForTable(table.toUpperCase());
        return ResponseEntity.ok(ApiResponse.success(columns));
    }

    @GetMapping("/relationships")
    public ResponseEntity<ApiResponse<List<ERDResponse.RelationshipDTO>>> getRelationships() {
        log.info("GET /api/schema/relationships");
        ERDResponse erd = tableMetadataService.getERD();
        return ResponseEntity.ok(ApiResponse.success(erd.relationships()));
    }

    @GetMapping("/erd")
    public ResponseEntity<ApiResponse<ERDResponse>> getERD() {
        log.info("GET /api/schema/erd");
        ERDResponse erd = tableMetadataService.getERD();
        return ResponseEntity.ok(ApiResponse.success(erd));
    }
}
