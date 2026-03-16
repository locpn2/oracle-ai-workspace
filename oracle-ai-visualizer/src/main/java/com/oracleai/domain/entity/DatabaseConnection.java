package com.oracleai.domain.entity;

import com.oracleai.domain.valueobject.*;
import java.util.UUID;

public class DatabaseConnection {
    private ConnectionId id;
    private UserId ownerId;
    private String name;
    private ConnectionConfig config;
    private ConnectionStatus status;
    private CreatedAt createdAt;
    private String errorMessage;

    private DatabaseConnection() {}

    public DatabaseConnection(ConnectionId id, UserId ownerId, String name, 
                              ConnectionConfig config, CreatedAt createdAt) {
        this.id = id;
        this.ownerId = ownerId;
        this.name = name;
        this.config = config;
        this.status = ConnectionStatus.DISCONNECTED;
        this.createdAt = createdAt;
    }

    public static DatabaseConnection create(UserId ownerId, String name, 
                                            String host, int port, String service,
                                            String username, String password) {
        return new DatabaseConnection(
            ConnectionId.generate(),
            ownerId,
            name,
            new ConnectionConfig(host, port, service, username, password),
            CreatedAt.now()
        );
    }

    public void markConnecting() {
        this.status = ConnectionStatus.CONNECTING;
    }

    public void markConnected() {
        this.status = ConnectionStatus.CONNECTED;
        this.errorMessage = null;
    }

    public void markError(String message) {
        this.status = ConnectionStatus.ERROR;
        this.errorMessage = message;
    }

    public void disconnect() {
        this.status = ConnectionStatus.DISCONNECTED;
    }

    public ConnectionId getId() { return id; }
    public UserId getOwnerId() { return ownerId; }
    public String getName() { return name; }
    public ConnectionConfig getConfig() { return config; }
    public ConnectionStatus getStatus() { return status; }
    public CreatedAt getCreatedAt() { return createdAt; }
    public String getErrorMessage() { return errorMessage; }
}
