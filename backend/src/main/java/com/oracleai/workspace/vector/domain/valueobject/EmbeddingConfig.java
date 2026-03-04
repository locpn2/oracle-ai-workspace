package com.oracleai.workspace.vector.domain.valueobject;

import java.time.Duration;

public record EmbeddingConfig(
    EmbeddingModel model,
    int batchSize,
    int maxRetries,
    Duration timeout
) {
    public static EmbeddingConfig defaultConfig() {
        return new EmbeddingConfig(
            EmbeddingModel.BGE_BASE,
            1000,
            3,
            Duration.ofMinutes(5)
        );
    }
}
