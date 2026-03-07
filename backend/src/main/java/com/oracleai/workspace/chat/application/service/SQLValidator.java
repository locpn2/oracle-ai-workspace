package com.oracleai.workspace.chat.application.service;

import com.oracleai.workspace.chat.domain.valueobject.ValidatedSQL;
import com.oracleai.workspace.shared.exception.ValidationException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class SQLValidator {

    private static final Logger log = LoggerFactory.getLogger(SQLValidator.class);

    // Invariant: C-SQL - SQL must be SELECT-only for security
    private static final Set<String> ALLOWED_PREFIXES = Set.of("SELECT", "WITH");
    
    private static final Set<String> FORBIDDEN_KEYWORDS = Set.of(
            "DROP", "DELETE", "INSERT", "UPDATE", "CREATE", "ALTER",
            "TRUNCATE", "EXEC", "EXECUTE", "GRANT", "REVOKE",
            "COMMIT", "ROLLBACK", "CALL", "MERGE", "BEGIN", "DECLARE"
    );
    
    private static final int MAX_LIMIT = 10000;

    public ValidatedSQL validate(String sql) {
        log.debug("Validating SQL: {}", sql);
        
        if (sql == null || sql.trim().isEmpty()) {
            throw new ValidationException("SQL cannot be empty");
        }

        String trimmed = sql.trim();
        String upper = trimmed.toUpperCase();

        // Rule 1: Must start with allowed prefix
        boolean allowedPrefix = ALLOWED_PREFIXES.stream()
                .anyMatch(upper::startsWith);
        
        if (!allowedPrefix) {
            throw new ValidationException("SQL must start with: SELECT or WITH");
        }

        // Rule 2: No forbidden keywords
        for (String keyword : FORBIDDEN_KEYWORDS) {
            Pattern pattern = Pattern.compile("\\b" + keyword + "\\b", Pattern.CASE_INSENSITIVE);
            if (pattern.matcher(upper).find()) {
                log.warn("Forbidden keyword detected: {}", keyword);
                throw new ValidationException("Forbidden keyword in SQL: " + keyword);
            }
        }

        // Rule 3: No UNION with dangerous queries
        if (upper.contains("UNION")) {
            String[] parts = upper.split("UNION");
            for (int i = 1; i < parts.length; i++) {
                String part = parts[i].trim();
                if (!part.startsWith("SELECT") && !part.startsWith("WITH")) {
                    throw new ValidationException("UNION must be followed by SELECT or WITH only");
                }
            }
        }

        // Rule 4: Max result rows limit
        int limit = extractLimit(upper);
        if (limit > MAX_LIMIT) {
            throw new ValidationException("LIMIT cannot exceed " + MAX_LIMIT + " rows");
        }

        // Extract referenced tables and columns
        Set<String> tables = extractReferencedTables(sql);
        Set<String> columns = extractReferencedColumns(sql);

        log.info("SQL validation passed - tables: {}, columns: {}", tables.size(), columns.size());
        
        return new ValidatedSQL(sql, com.oracleai.workspace.chat.domain.valueobject.SQLType.SELECT, tables, columns);
    }

    private int extractLimit(String sql) {
        Pattern limitPattern = Pattern.compile("LIMIT\\s+(\\d+)", Pattern.CASE_INSENSITIVE);
        Matcher m = limitPattern.matcher(sql);
        if (m.find()) {
            return Integer.parseInt(m.group(1));
        }
        return 0;
    }

    private Set<String> extractReferencedTables(String sql) {
        Set<String> tables = new HashSet<>();
        
        // Match FROM and JOIN clauses
        Pattern fromPattern = Pattern.compile(
            "(?:FROM|JOIN|INTO|UPDATE)\\s+(\\w+)", 
            Pattern.CASE_INSENSITIVE
        );
        
        Matcher matcher = fromPattern.matcher(sql);
        while (matcher.find()) {
            String tableName = matcher.group(1).toUpperCase();
            if (!isKeyword(tableName)) {
                tables.add(tableName);
            }
        }
        
        return tables;
    }

    private Set<String> extractReferencedColumns(String sql) {
        Set<String> columns = new HashSet<>();
        
        // Match column names after SELECT, WHERE, ON, etc.
        Pattern columnPattern = Pattern.compile(
            "(?:SELECT|ON|WHERE|AND|OR|=|<|>|<=|>=|!=)\\s+(\\w+(?:\\.\\w+)?)",
            Pattern.CASE_INSENSITIVE
        );
        
        Matcher matcher = columnPattern.matcher(sql);
        while (matcher.find()) {
            String col = matcher.group(1);
            if (!isKeyword(col) && col.contains(".")) {
                columns.add(col.toUpperCase());
            } else if (!isKeyword(col)) {
                columns.add(col.toUpperCase());
            }
        }
        
        return columns;
    }

    private boolean isKeyword(String word) {
        Set<String> keywords = Set.of(
            "SELECT", "FROM", "WHERE", "AND", "OR", "NOT", "IN", "LIKE",
            "BETWEEN", "IS", "NULL", "TRUE", "FALSE", "AS", "ON", "JOIN",
            "LEFT", "RIGHT", "INNER", "OUTER", "FULL", "CROSS", "UNION",
            "ORDER", "BY", "GROUP", "HAVING", "LIMIT", "OFFSET", "WITH",
            "CASE", "WHEN", "THEN", "ELSE", "END", "EXISTS", "ANY", "ALL"
        );
        return keywords.contains(word.toUpperCase());
    }
}
