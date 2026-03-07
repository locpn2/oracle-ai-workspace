package com.oracleai.workspace.schema.infrastructure.oracle;

import com.oracleai.workspace.schema.domain.entity.Table;
import com.oracleai.workspace.schema.domain.repository.TableRepository;
import com.oracleai.workspace.schema.domain.valueobject.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Repository;

import java.sql.*;
import java.util.*;
import java.util.stream.Collectors;

@Repository
public class OracleSchemaExtractor implements TableRepository {

    private static final Logger log = LoggerFactory.getLogger(OracleSchemaExtractor.class);

    // In-memory cache for development
    private final Map<String, Table> tableCache = new HashMap<>();

    @Override
    public List<Table> findAll() {
        log.info("Extracting all tables from Oracle");
        // In production, query Oracle metadata
        // For now, return cached tables
        return new ArrayList<>(tableCache.values());
    }

    @Override
    public Optional<Table> findByName(TableName name) {
        log.info("Finding table: {}", name.value());
        return Optional.ofNullable(tableCache.get(name.value()));
    }

    @Override
    public List<String> findAllTableNames() {
        log.info("Getting all table names");
        return tableCache.keySet().stream().sorted().collect(Collectors.toList());
    }

    public void refreshCache(Connection connection) throws SQLException {
        log.info("Refreshing schema cache from Oracle");
        tableCache.clear();

        // Get tables
        String tablesSql = """
            SELECT table_name, table_type 
            FROM user_tables 
            UNION 
            SELECT view_name AS table_name, 'VIEW' AS table_type 
            FROM user_views
            ORDER BY table_name
            """;
        
        try (Statement stmt = connection.createStatement();
             ResultSet rs = stmt.executeQuery(tablesSql)) {
            
            while (rs.next()) {
                String tableName = rs.getString("table_name");
                String tableType = rs.getString("table_type");
                
                // Get columns
                List<Column> columns = getColumns(connection, tableName);
                
                // Get primary key
                PrimaryKey pk = getPrimaryKey(connection, tableName);
                
                // Get foreign keys
                List<ForeignKey> fks = getForeignKeys(connection, tableName);
                
                Table table = Table.builder()
                        .name(new TableName(tableName))
                        .type(TableType.valueOf(tableType))
                        .columns(columns)
                        .primaryKey(pk)
                        .foreignKeys(fks)
                        .build();
                
                tableCache.put(tableName, table);
            }
        }
        
        log.info("Loaded {} tables from Oracle", tableCache.size());
    }

    private List<Column> getColumns(Connection connection, String tableName) throws SQLException {
        String sql = """
            SELECT column_name, data_type, data_length, data_precision, data_scale, 
                   nullable, column_id, data_default
            FROM user_tab_columns
            WHERE table_name = ?
            ORDER BY column_id
            """;
        
        List<Column> columns = new ArrayList<>();
        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setString(1, tableName);
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    String colName = rs.getString("column_name");
                    String dataType = rs.getString("data_type");
                    boolean nullable = "Y".equals(rs.getString("nullable"));
                    int position = rs.getInt("column_id");
                    String defaultValue = rs.getString("data_default");
                    
                    DataType dtype = mapDataType(dataType);
                    
                    Column column = new Column(
                            new ColumnName(colName),
                            dtype,
                            nullable,
                            position,
                            defaultValue
                    );
                    columns.add(column);
                }
            }
        }
        return columns;
    }

    private PrimaryKey getPrimaryKey(Connection connection, String tableName) throws SQLException {
        String sql = """
            SELECT a.constraint_name, a.column_name
            FROM user_cons_columns a
            JOIN user_constraints b ON a.constraint_name = b.constraint_name
            WHERE b.table_name = ? AND b.constraint_type = 'P'
            ORDER BY a.position
            """;
        
        List<ColumnName> pkColumns = new ArrayList<>();
        String pkName = null;
        
        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setString(1, tableName);
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    if (pkName == null) {
                        pkName = rs.getString("constraint_name");
                    }
                    pkColumns.add(new ColumnName(rs.getString("column_name")));
                }
            }
        }
        
        if (pkColumns.isEmpty()) {
            return null;
        }
        
        return new PrimaryKey(pkColumns, new ConstraintName(pkName));
    }

    private List<ForeignKey> getForeignKeys(Connection connection, String tableName) throws SQLException {
        String sql = """
            SELECT a.constraint_name, 
                   a.column_name AS source_column,
                   c.table_name AS target_table,
                   c.column_name AS target_column,
                   b.delete_rule
            FROM user_cons_columns a
            JOIN user_constraints b ON a.constraint_name = b.constraint_name
            JOIN user_constraints c ON b.r_constraint_name = c.constraint_name
            JOIN user_cons_columns d ON c.constraint_name = d.constraint_name AND d.position = a.position
            WHERE b.table_name = ? AND b.constraint_type = 'R'
            ORDER BY a.position
            """;
        
        Map<String, ForeignKey.Builder> fkBuilders = new LinkedHashMap<>();
        
        try (PreparedStatement pstmt = connection.prepareStatement(sql)) {
            pstmt.setString(1, tableName);
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    String fkName = rs.getString("constraint_name");
                    String sourceCol = rs.getString("source_column");
                    String targetTable = rs.getString("target_table");
                    String targetCol = rs.getString("target_column");
                    String deleteRule = rs.getString("delete_rule");
                    
                    ForeignKey.Builder builder = fkBuilders.computeIfAbsent(fkName, 
                            name -> ForeignKey.builder()
                                    .name(new ConstraintName(name))
                                    .targetTable(new TableName(targetTable))
                                    .deleteRule(DeleteRule.valueOf(deleteRule != null ? deleteRule : "NO_ACTION")));
                    
                    builder.addSourceColumn(new ColumnName(sourceCol));
                    builder.addTargetColumn(new ColumnName(targetCol));
                }
            }
        }
        
        return fkBuilders.values().stream()
                .map(ForeignKey.Builder::build)
                .collect(Collectors.toList());
    }

    private DataType mapDataType(String oracleType) {
        if (oracleType == null) return DataType.VARCHAR2;
        return switch (oracleType.toUpperCase()) {
            case "VARCHAR2", "VARCHAR", "CHAR", "NCHAR", "NVARCHAR2" -> DataType.VARCHAR2;
            case "NUMBER", "INTEGER", "INT", "SMALLINT", "FLOAT", "DOUBLE", "BINARY_FLOAT", "BINARY_DOUBLE" -> DataType.NUMBER;
            case "DATE" -> DataType.DATE;
            case "TIMESTAMP", "TIMESTAMP WITH TIME ZONE", "TIMESTAMP WITH LOCAL TIME ZONE" -> DataType.TIMESTAMP;
            case "BLOB", "RAW", "LONG RAW" -> DataType.BLOB;
            case "CLOB", "NCLOB", "LONG" -> DataType.CLOB;
            case "ROWID" -> DataType.ROWID;
            default -> DataType.VARCHAR2;
        };
    }
}
