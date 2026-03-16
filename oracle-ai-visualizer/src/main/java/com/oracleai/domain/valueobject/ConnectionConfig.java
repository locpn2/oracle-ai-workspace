package com.oracleai.domain.valueobject;

public record ConnectionConfig(
    String host,
    int port,
    String service,
    String username,
    String password
) {
    public ConnectionConfig {
        if (host == null || host.isBlank()) {
            throw new IllegalArgumentException("Host cannot be blank");
        }
        if (service == null || service.isBlank()) {
            throw new IllegalArgumentException("Service cannot be blank");
        }
        if (username == null || username.isBlank()) {
            throw new IllegalArgumentException("Username cannot be blank");
        }
    }

    public String toJdbcUrl() {
        return String.format("jdbc:oracle:thin:@//%s:%d/%s", host, port, service);
    }
}
