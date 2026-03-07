package com.oracleai.workspace.schema.domain.entity;

import com.oracleai.workspace.schema.domain.valueobject.*;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

class TableTest {

    @Test
    void createTable_WithValidData_ReturnsTable() {
        Column idColumn = new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null);
        Column nameColumn = new Column(new ColumnName("NAME"), DataType.VARCHAR2, true, 2, null);
        
        Table table = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(idColumn, nameColumn))
                .type(TableType.TABLE)
                .rowCount(100)
                .build();

        assertNotNull(table);
        assertEquals("USERS", table.getName().value());
        assertEquals(2, table.getColumns().size());
        assertEquals(TableType.TABLE, table.getType());
        assertEquals(100, table.getRowCount());
    }

    @Test
    void createTable_WithoutName_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () ->
                Table.builder()
                        .columns(List.of(new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null)))
                        .build()
        );
    }

    @Test
    void hasColumn_WithExistingColumn_ReturnsTrue() {
        Table table = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null),
                        new Column(new ColumnName("NAME"), DataType.VARCHAR2, true, 2, null)
                ))
                .build();

        assertTrue(table.hasColumn(new ColumnName("ID")));
        assertTrue(table.hasColumn(new ColumnName("NAME")));
    }

    @Test
    void hasColumn_WithNonExistingColumn_ReturnsFalse() {
        Table table = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null)))
                .build();

        assertFalse(table.hasColumn(new ColumnName("EMAIL")));
    }

    @Test
    void findColumn_WhenExists_ReturnsColumn() {
        Column nameColumn = new Column(new ColumnName("NAME"), DataType.VARCHAR2, true, 2, null);
        Table table = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null),
                        nameColumn
                ))
                .build();

        Optional<Column> result = table.findColumn(new ColumnName("NAME"));

        assertTrue(result.isPresent());
        assertEquals("NAME", result.get().name().value());
    }

    @Test
    void findForeignKeyTo_WithMatchingFK_ReturnsFK() {
        TableName usersTableName = new TableName("USERS");
        
        ForeignKey fk = ForeignKey.builder()
                .name(new ConstraintName("FK_orders_user"))
                .addSourceColumn(new ColumnName("USER_ID"))
                .targetTable(usersTableName)
                .addTargetColumn(new ColumnName("ID"))
                .build();

        Table ordersTable = Table.builder()
                .name(new TableName("ORDERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null),
                        new Column(new ColumnName("USER_ID"), DataType.NUMBER, false, 2, null)
                ))
                .foreignKeys(List.of(fk))
                .build();

        Optional<ForeignKey> result = ordersTable.findForeignKeyTo(usersTableName);

        assertTrue(result.isPresent());
    }

    @Test
    void getColumnNames_ReturnsAllColumnNames() {
        Table table = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null),
                        new Column(new ColumnName("NAME"), DataType.VARCHAR2, true, 2, null),
                        new Column(new ColumnName("EMAIL"), DataType.VARCHAR2, true, 3, null)
                ))
                .build();

        List<ColumnName> columnNames = table.getColumnNames();

        assertEquals(3, columnNames.size());
        assertTrue(columnNames.contains(new ColumnName("ID")));
        assertTrue(columnNames.contains(new ColumnName("NAME")));
        assertTrue(columnNames.contains(new ColumnName("EMAIL")));
    }
}
