package com.oracleai.workspace.vector.application.service;

import com.oracleai.workspace.schema.application.dto.ColumnDTO;
import com.oracleai.workspace.schema.application.dto.TableDTO;
import com.oracleai.workspace.schema.application.service.TableMetadataService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class FlatteningService {

    private static final Logger log = LoggerFactory.getLogger(FlatteningService.class);

    private final TableMetadataService tableMetadataService;

    public FlatteningService(TableMetadataService tableMetadataService) {
        this.tableMetadataService = tableMetadataService;
    }

    public String flattenRow(Map<String, Object> row, String tableName) {
        log.debug("Flattening row for table: {}", tableName);
        
        TableDTO table = tableMetadataService.getTableByName(tableName);
        if (table == null) {
            throw new IllegalArgumentException("Table not found: " + tableName);
        }

        StringBuilder document = new StringBuilder();
        
        for (ColumnDTO column : table.columns()) {
            Object value = row.get(column.name());
            
            if (value == null) {
                continue; // Invariant: V2 - Skip NULL values
            }
            
            // Skip BLOB/CLOB
            if (isBinaryType(column.dataType())) {
                continue;
            }
            
            // Sanitize special characters - Invariant: Data quality
            String sanitizedValue = sanitize(String.valueOf(value));
            
            document.append(column.name())
                    .append(": ")
                    .append(sanitizedValue)
                    .append(", ");
        }
        
        // Remove trailing comma and space
        if (document.length() > 2) {
            document.setLength(document.length() - 2);
        }
        
        return document.toString();
    }

    private boolean isBinaryType(String dataType) {
        return "BLOB".equalsIgnoreCase(dataType) || 
               "CLOB".equalsIgnoreCase(dataType) ||
               "NCLOB".equalsIgnoreCase(dataType);
    }

    private String sanitize(String value) {
        if (value == null) return "";
        // Remove control characters and excessive whitespace
        return value.replaceAll("[\\p{Cntrl}]", " ")
                    .replaceAll("\\s+", " ")
                    .trim();
    }
}
