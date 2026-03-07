package com.oracleai.workspace.chat.application;

import com.oracleai.workspace.chat.application.service.SQLValidator;
import com.oracleai.workspace.chat.domain.valueobject.ValidatedSQL;
import com.oracleai.workspace.chat.domain.valueobject.SQLType;
import com.oracleai.workspace.shared.exception.ValidationException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SQLValidatorTest {

    private SQLValidator sqlValidator;

    @BeforeEach
    void setUp() {
        sqlValidator = new SQLValidator();
    }

    @Test
    void validate_WithSimpleSelect_ReturnsValidatedSQL() {
        String sql = "SELECT * FROM users";
        
        ValidatedSQL result = sqlValidator.validate(sql);
        
        assertNotNull(result);
        assertEquals(SQLType.SELECT, result.type());
        assertTrue(result.referencedTables().contains("USERS"));
    }

    @Test
    void validate_WithCTE_ReturnsValidatedSQL() {
        String sql = "WITH cte AS (SELECT id FROM users) SELECT * FROM cte";
        
        ValidatedSQL result = sqlValidator.validate(sql);
        
        assertNotNull(result);
        assertTrue(result.referencedTables().contains("USERS"));
    }

    @Test
    void validate_WithNullSQL_ThrowsException() {
        assertThrows(ValidationException.class, () -> sqlValidator.validate(null));
    }

    @Test
    void validate_WithEmptySQL_ThrowsException() {
        assertThrows(ValidationException.class, () -> sqlValidator.validate("   "));
    }

    @Test
    void validate_WithInsert_ThrowsException() {
        String sql = "INSERT INTO users VALUES (1, 'John')";
        
        assertThrows(ValidationException.class, () -> sqlValidator.validate(sql));
    }

    @Test
    void validate_WithDelete_ThrowsException() {
        String sql = "DELETE FROM users WHERE id = 1";
        
        assertThrows(ValidationException.class, () -> sqlValidator.validate(sql));
    }

    @Test
    void validate_WithUpdate_ThrowsException() {
        String sql = "UPDATE users SET name = 'John' WHERE id = 1";
        
        assertThrows(ValidationException.class, () -> sqlValidator.validate(sql));
    }

    @Test
    void validate_WithDrop_ThrowsException() {
        String sql = "DROP TABLE users";
        
        assertThrows(ValidationException.class, () -> sqlValidator.validate(sql));
    }

    @Test
    void validate_WithUnion_ValidatesBothParts() {
        String sql = "SELECT id FROM users UNION SELECT id FROM admins";
        
        ValidatedSQL result = sqlValidator.validate(sql);
        
        assertNotNull(result);
        assertTrue(result.referencedTables().contains("USERS"));
        assertTrue(result.referencedTables().contains("ADMINS"));
    }

    @Test
    void validate_WithInvalidUnion_ThrowsException() {
        String sql = "SELECT id FROM users UNION INSERT INTO users VALUES (1)";
        
        assertThrows(ValidationException.class, () -> sqlValidator.validate(sql));
    }

    @Test
    void validate_WithLimitWithinRange_ReturnsValidatedSQL() {
        String sql = "SELECT * FROM users LIMIT 100";
        
        ValidatedSQL result = sqlValidator.validate(sql);
        
        assertNotNull(result);
    }

    @Test
    void validate_WithLimitExceedingMax_ThrowsException() {
        String sql = "SELECT * FROM users LIMIT 20000";
        
        assertThrows(ValidationException.class, () -> sqlValidator.validate(sql));
    }

    @Test
    void validate_WithJoin_ReturnsTablesAndColumns() {
        String sql = "SELECT u.id, u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id";
        
        ValidatedSQL result = sqlValidator.validate(sql);
        
        assertNotNull(result);
        assertTrue(result.referencedTables().contains("USERS"));
        assertTrue(result.referencedTables().contains("ORDERS"));
    }

    @Test
    void validate_WithSubquery_ReturnsValidatedSQL() {
        String sql = "SELECT * FROM users WHERE id IN (SELECT user_id FROM orders)";
        
        ValidatedSQL result = sqlValidator.validate(sql);
        
        assertNotNull(result);
        assertTrue(result.referencedTables().contains("USERS"));
        assertTrue(result.referencedTables().contains("ORDERS"));
    }
}
