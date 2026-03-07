package com.oracleai.workspace.shared.exception;

public class NotFoundException extends DomainException {
    
    public NotFoundException(String resource, String identifier) {
        super("NOT_FOUND", resource + " not found: " + identifier);
    }

    public NotFoundException(String message) {
        super("NOT_FOUND", message);
    }
}
