package com.oracleai.workspace.vector.application.service;

import com.oracleai.workspace.vector.domain.valueobject.EmbeddingModel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.List;
import java.util.Map;

@Service
public class EmbeddingService {

    private static final Logger log = LoggerFactory.getLogger(EmbeddingService.class);
    private static final int EMBEDDING_DIMENSION = 768;

    private final RestClient restClient;

    @Value("${ollama.base-url:http://localhost:11434}")
    private String ollamaBaseUrl;

    @Value("${ollama.embedding-model:bge-base}")
    private String embeddingModel;

    public EmbeddingService() {
        this.restClient = RestClient.builder().build();
    }

    public float[] generateEmbedding(String text) {
        log.debug("Generating embedding for text of length: {}", text.length());
        
        try {
            return callOllamaEmbedding(text);
        } catch (Exception e) {
            log.warn("Ollama embedding failed: {}", e.getMessage());
            throw new RuntimeException("Failed to generate embedding: " + e.getMessage());
        }
    }

    public List<float[]> generateEmbeddings(List<String> texts) {
        log.info("Generating embeddings for {} texts", texts.size());
        return texts.stream()
                .map(this::generateEmbedding)
                .toList();
    }

    private float[] callOllamaEmbedding(String text) {
        log.debug("Calling Ollama for embedding");
        
        Map<String, Object> request = Map.of(
            "model", embeddingModel,
            "input", text
        );
        
        @SuppressWarnings("unchecked")
        Map<String, Object> response = restClient.post()
                .uri(ollamaBaseUrl + "/api/embeddings")
                .header("Content-Type", "application/json")
                .body(request)
                .retrieve()
                .body(Map.class);
        
        @SuppressWarnings("unchecked")
        List<Number> embedding = (List<Number>) response.get("embedding");
        
        float[] result = new float[embedding.size()];
        for (int i = 0; i < embedding.size(); i++) {
            result[i] = embedding.get(i).floatValue();
        }
        
        // Invariant: V1 - Validate embedding dimension
        if (result.length != EMBEDDING_DIMENSION) {
            throw new IllegalStateException("Invalid embedding dimension: " + result.length + 
                    ", expected: " + EMBEDDING_DIMENSION);
        }
        
        return result;
    }

    public int getDimension() {
        return EMBEDDING_DIMENSION;
    }
}
