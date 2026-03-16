package com.oracleai.domain.entity;

import com.oracleai.domain.valueobject.*;
import java.util.List;
import java.util.Map;
import java.util.UUID;

public class Query {
    private QueryId id;
    private UserId userId;
    private ConnectionId connectionId;
    private String question;
    private String generatedSql;
    private QueryStatus status;
    private QueryResult result;
    private String errorMessage;
    private CreatedAt createdAt;

    private Query() {}

    public Query(QueryId id, UserId userId, ConnectionId connectionId, String question, CreatedAt createdAt) {
        this.id = id;
        this.userId = userId;
        this.connectionId = connectionId;
        this.question = question;
        this.status = QueryStatus.PENDING;
        this.createdAt = createdAt;
    }

    public static Query create(UserId userId, ConnectionId connectionId, String question) {
        return new Query(
            QueryId.generate(),
            userId,
            connectionId,
            question,
            CreatedAt.now()
        );
    }

    public void setGeneratedSql(String sql) {
        this.generatedSql = sql;
        this.status = QueryStatus.SQL_GENERATED;
    }

    public void markExecuting() {
        this.status = QueryStatus.EXECUTING;
    }

    public void markCompleted(QueryResult result) {
        this.status = QueryStatus.COMPLETED;
        this.result = result;
    }

    public void markFailed(String error) {
        this.status = QueryStatus.FAILED;
        this.errorMessage = error;
    }

    public QueryId getId() { return id; }
    public UserId getUserId() { return userId; }
    public ConnectionId getConnectionId() { return connectionId; }
    public String getQuestion() { return question; }
    public String getGeneratedSql() { return generatedSql; }
    public QueryStatus getStatus() { return status; }
    public QueryResult getResult() { return result; }
    public String getErrorMessage() { return errorMessage; }
    public CreatedAt getCreatedAt() { return createdAt; }

    public record QueryId(UUID value) {
        public static QueryId generate() { return new QueryId(UUID.randomUUID()); }
    }

    public enum QueryStatus {
        PENDING,
        SQL_GENERATED,
        EXECUTING,
        COMPLETED,
        FAILED
    }

    public record QueryResult(
        List<String> columns,
        List<Map<String, Object>> rows,
        int rowCount
    ) {
        public static QueryResult empty() {
            return new QueryResult(List.of(), List.of(), 0);
        }
    }
}
