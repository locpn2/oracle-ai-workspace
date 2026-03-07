package com.oracleai.workspace.shared.exception;

public class ValidationException extends DomainException {
    
    public ValidationException(String message) {
        super("VALIDATION_ERROR", message);
    }

    public ValidationException(String field, String message) {
        super("VALIDATION_ERROR", field + ": " + message);
    }
}
