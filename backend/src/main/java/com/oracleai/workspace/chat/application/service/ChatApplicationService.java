package com.oracleai.workspace.chat.application.service;

import com.oracleai.workspace.chat.application.dto.QueryRequest;
import com.oracleai.workspace.chat.application.dto.QueryResponse;
import com.oracleai.workspace.chat.application.port.in.QueryUseCase;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ChatApplicationService implements QueryUseCase {

    private static final Logger log = LoggerFactory.getLogger(ChatApplicationService.class);

    private final TextToSQLService textToSQLService;
    private final SQLValidator sqlValidator;

    public ChatApplicationService(TextToSQLService textToSQLService, SQLValidator sqlValidator) {
        this.textToSQLService = textToSQLService;
        this.sqlValidator = sqlValidator;
    }

    @Override
    public QueryResponse processQuery(QueryRequest request) {
        log.info("Processing chat query: {}", request.message());
        
        try {
            String sql = textToSQLService.generateSQL(request.message());
            
            var validated = sqlValidator.validate(sql);
            
            return QueryResponse.success(
                request.sessionId(),
                request.message(),
                sql,
                0,
                List.copyOf(validated.referencedColumns()),
                List.of(),
                "groq"
            );
        } catch (Exception e) {
            log.error("Error processing query: {}", e.getMessage());
            return QueryResponse.error(
                request.sessionId(),
                request.message(),
                e.getMessage()
            );
        }
    }
}
