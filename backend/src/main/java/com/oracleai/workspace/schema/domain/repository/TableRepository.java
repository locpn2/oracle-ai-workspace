package com.oracleai.workspace.schema.domain.repository;

import com.oracleai.workspace.schema.domain.entity.Table;
import com.oracleai.workspace.schema.domain.valueobject.TableName;

import java.util.List;
import java.util.Optional;

public interface TableRepository {
    List<Table> findAll();
    Optional<Table> findByName(TableName name);
    List<String> findAllTableNames();
}
