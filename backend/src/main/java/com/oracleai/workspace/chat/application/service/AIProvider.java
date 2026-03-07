package com.oracleai.workspace.chat.application.service;

public enum AIProvider {
    GROQ("Groq", "llama-3.1-8b-instant"),
    OLLAMA("Ollama", "sqlcoder:7b"),
    GEMINI("Gemini", "gemini-2.0-flash");

    private final String displayName;
    private final String defaultModel;

    AIProvider(String displayName, String defaultModel) {
        this.displayName = displayName;
        this.defaultModel = defaultModel;
    }

    public String getDisplayName() { return displayName; }
    public String getDefaultModel() { return defaultModel; }
}
