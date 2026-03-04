package com.oracleai.workspace.vector.domain.valueobject;

public record SearchResult(
    VectorEntry entry,
    double similarityScore,
    String highlightedText
) {
    public static SearchResult of(VectorEntry entry, double score) {
        return new SearchResult(entry, score, entry.document());
    }
}
