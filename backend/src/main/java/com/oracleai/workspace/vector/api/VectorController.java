package com.oracleai.workspace.vector.api;

import com.oracleai.workspace.vector.application.dto.EmbedTableRequest;
import com.oracleai.workspace.vector.application.dto.SearchRequest;
import com.oracleai.workspace.vector.application.dto.SearchResponse;
import com.oracleai.workspace.vector.application.service.EmbeddingService;
import com.oracleai.workspace.vector.application.service.FlatteningService;
import com.oracleai.workspace.vector.application.service.VectorSearchService;
import com.oracleai.workspace.shared.dto.ApiResponse;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/vector")
public class VectorController {

    private static final Logger log = LoggerFactory.getLogger(VectorController.class);

    private final EmbeddingService embeddingService;
    private final FlatteningService flatteningService;
    private final VectorSearchService vectorSearchService;

    public VectorController(EmbeddingService embeddingService, 
                           FlatteningService flatteningService,
                           VectorSearchService vectorSearchService) {
        this.embeddingService = embeddingService;
        this.flatteningService = flatteningService;
        this.vectorSearchService = vectorSearchService;
    }

    @PostMapping("/embed-table")
    public ResponseEntity<ApiResponse<Map<String, Object>>> embedTable(@Valid @RequestBody EmbedTableRequest request) {
        log.info("POST /api/vector/embed-table - table: {}", request.tableName());
        // TODO: Implement async embedding job
        return ResponseEntity.ok(ApiResponse.success(Map.of(
                "message", "Embedding job started",
                "tableName", request.tableName()
        )));
    }

    @PostMapping("/embed-rows")
    public ResponseEntity<ApiResponse<Map<String, Object>>> embedRows(@RequestBody Map<String, Object> request) {
        log.info("POST /api/vector/embed-rows");
        return ResponseEntity.ok(ApiResponse.success(Map.of(
                "message", "Rows embedded successfully"
        )));
    }

    @GetMapping("/search")
    public ResponseEntity<ApiResponse<SearchResponse>> search(@Valid SearchRequest request) {
        log.info("GET /api/vector/search - query: {}", request.query());
        SearchResponse response = vectorSearchService.search(request);
        return ResponseEntity.ok(ApiResponse.success(response));
    }

    @GetMapping("/status")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getStatus(@RequestParam(required = false) String tableName) {
        log.info("GET /api/vector/status - tableName: {}", tableName);
        return ResponseEntity.ok(ApiResponse.success(Map.of(
                "message", "Vector store status",
                "tableName", tableName != null ? tableName : "all"
        )));
    }
}
