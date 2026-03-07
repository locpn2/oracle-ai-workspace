package com.oracleai.workspace.chat.application.port.in;

import com.oracleai.workspace.chat.application.dto.QueryRequest;
import com.oracleai.workspace.chat.application.dto.QueryResponse;

public interface QueryUseCase {
    QueryResponse processQuery(QueryRequest request);
}
