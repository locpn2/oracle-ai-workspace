package com.oracleai.workspace.chat.api;

import com.oracleai.workspace.chat.application.dto.QueryRequest;
import com.oracleai.workspace.chat.application.dto.QueryResponse;
import com.oracleai.workspace.chat.application.port.in.QueryUseCase;
import com.oracleai.workspace.shared.dto.ApiResponse;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/chat")
public class ChatController {

    private static final Logger log = LoggerFactory.getLogger(ChatController.class);

    private final QueryUseCase queryUseCase;

    public ChatController(QueryUseCase queryUseCase) {
        this.queryUseCase = queryUseCase;
    }

    @PostMapping("/query")
    public ResponseEntity<ApiResponse<QueryResponse>> processQuery(@Valid @RequestBody QueryRequest request) {
        log.info("POST /api/chat/query - message: {}", request.message());
        QueryResponse response = queryUseCase.processQuery(request);
        
        if (response.success()) {
            return ResponseEntity.ok(ApiResponse.success(response, "Query executed successfully"));
        } else {
            return ResponseEntity.badRequest().body(ApiResponse.error(response.errorMessage(), "QUERY_ERROR"));
        }
    }

    @GetMapping("/history")
    public ResponseEntity<ApiResponse<Object>> getChatHistory() {
        log.info("GET /api/chat/history");
        // TODO: Implement chat history retrieval
        return ResponseEntity.ok(ApiResponse.success(null, "Chat history"));
    }

    @GetMapping("/history/{sessionId}")
    public ResponseEntity<ApiResponse<Object>> getSessionHistory(@PathVariable String sessionId) {
        log.info("GET /api/chat/history/{}", sessionId);
        // TODO: Implement session history retrieval
        return ResponseEntity.ok(ApiResponse.success(null, "Session history"));
    }
}
