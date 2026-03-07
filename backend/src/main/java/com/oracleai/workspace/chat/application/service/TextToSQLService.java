package com.oracleai.workspace.chat.application.service;

import com.oracleai.workspace.chat.application.dto.QueryResponse;
import com.oracleai.workspace.schema.application.dto.ERDResponse;
import com.oracleai.workspace.schema.application.service.TableMetadataService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Map;

@Service
public class TextToSQLService {

    private static final Logger log = LoggerFactory.getLogger(TextToSQLService.class);

    private final TableMetadataService tableMetadataService;
    private final SQLValidator sqlValidator;
    private final RestClient restClient;

    @Value("${groq.api-key:}")
    private String groqApiKey;

    @Value("${groq.model:llama-3.1-8b-instant}")
    private String groqModel;

    private static final String GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions";

    public TextToSQLService(TableMetadataService tableMetadataService, SQLValidator sqlValidator) {
        this.tableMetadataService = tableMetadataService;
        this.sqlValidator = sqlValidator;
        this.restClient = RestClient.builder().build();
    }

    public String generateSQL(String userQuestion) {
        log.info("Generating SQL for question: {}", userQuestion);
        
        // Get schema context
        ERDResponse erd = tableMetadataService.getERD();
        String schemaContext = buildSchemaContext(erd);
        
        // Build prompt
        String prompt = buildPrompt(userQuestion, schemaContext);
        
        // Try Groq first (primary)
        try {
            return callGroq(prompt);
        } catch (Exception e) {
            log.warn("Groq failed, trying Ollama: {}", e.getMessage());
            try {
                return callOllama(prompt);
            } catch (Exception e2) {
                log.warn("Ollama failed, trying Gemini: {}", e2.getMessage());
                return callGemini(prompt);
            }
        }
    }

    private String buildSchemaContext(ERDResponse erd) {
        StringBuilder sb = new StringBuilder();
        sb.append("Database Schema:\n\n");
        
        for (var table : erd.tables()) {
            sb.append("Table: ").append(table.name()).append("\n");
            sb.append("Columns:\n");
            for (var col : table.columns()) {
                sb.append("  - ").append(col.name()).append(" (").append(col.dataType());
                if (!col.nullable()) sb.append(", NOT NULL");
                sb.append(")\n");
            }
            if (table.primaryKey() != null) {
                sb.append("Primary Key: ").append(String.join(", ", table.primaryKey().columns())).append("\n");
            }
            sb.append("\n");
        }
        
        return sb.toString();
    }

    private String buildPrompt(String question, String schemaContext) {
        return String.format("""
            You are an expert SQL developer. Convert the question to Oracle SQL.
            
            %s
            
            Question: %s
            
            Rules:
            1. Use Oracle SQL syntax
            2. Only SELECT queries (no INSERT/UPDATE/DELETE)
            3. Use proper JOINs for multi-table queries
            4. Include appropriate WHERE clauses
            5. Use aggregate functions with GROUP BY when needed
            6. Add LIMIT clause with reasonable value (max 1000)
            
            Generate only the SQL query, no explanation.
            """, schemaContext, question);
    }

    private String callGroq(String prompt) {
        log.info("Calling Groq API");
        
        Map<String, Object> request = Map.of(
            "model", groqModel,
            "messages", new Object[] {
                Map.of("role", "user", "content", prompt)
            },
            "temperature", 0.0
        );
        
        @SuppressWarnings("unchecked")
        Map<String, Object> response = restClient.post()
                .uri(GROQ_API_URL)
                .header("Authorization", "Bearer " + groqApiKey)
                .header("Content-Type", "application/json")
                .body(request)
                .retrieve()
                .body(Map.class);
        
        @SuppressWarnings("unchecked")
        var choices = (java.util.List<Map<String, Object>>) response.get("choices");
        Map<String, Object> firstChoice = (Map<String, Object>) choices.get(0);
        Map<String, Object> message = (Map<String, Object>) firstChoice.get("message");
        return (String) message.get("content");
    }

    private String callOllama(String prompt) {
        log.info("Calling Ollama API");
        // Simplified - actual implementation would call local Ollama
        throw new RuntimeException("Ollama not configured");
    }

    private String callGemini(String prompt) {
        log.info("Calling Gemini API");
        // Simplified - actual implementation would call Gemini
        throw new RuntimeException("Gemini not configured");
    }
}
