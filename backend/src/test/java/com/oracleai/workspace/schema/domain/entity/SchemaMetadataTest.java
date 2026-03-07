package com.oracleai.workspace.schema.domain.entity;

import com.oracleai.workspace.schema.domain.valueobject.*;
import org.junit.jupiter.api.Test;

import java.time.Instant;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class SchemaMetadataTest {

    @Test
    void createSchemaMetadata_WithValidData_ReturnsSchema() {
        Table usersTable = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null),
                        new Column(new ColumnName("NAME"), DataType.VARCHAR2, true, 2, null)
                ))
                .build();

        SchemaMetadata schema = SchemaMetadata.builder()
                .ownerId("user123")
                .tables(List.of(usersTable))
                .build();

        assertNotNull(schema);
        assertEquals("user123", schema.getOwnerId());
        assertEquals(1, schema.getTableCount());
    }

    @Test
    void createSchemaMetadata_WithoutOwnerId_ThrowsException() {
        Table table = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null)
                ))
                .build();

        assertThrows(IllegalArgumentException.class, () ->
                SchemaMetadata.builder()
                        .tables(List.of(table))
                        .build()
        );
    }

    @Test
    void createSchemaMetadata_WithoutTables_ThrowsException() {
        assertThrows(IllegalArgumentException.class, () ->
                SchemaMetadata.builder()
                        .ownerId("user123")
                        .build()
        );
    }

    @Test
    void getTable_WhenExists_ReturnsTable() {
        Table usersTable = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null)
                ))
                .build();

        SchemaMetadata schema = SchemaMetadata.builder()
                .ownerId("user123")
                .tables(List.of(usersTable))
                .build();

        var result = schema.getTable(new TableName("USERS"));

        assertTrue(result.isPresent());
        assertEquals("USERS", result.get().getName().value());
    }

    @Test
    void hasTable_WhenExists_ReturnsTrue() {
        Table usersTable = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null)
                ))
                .build();

        SchemaMetadata schema = SchemaMetadata.builder()
                .ownerId("user123")
                .tables(List.of(usersTable))
                .build();

        assertTrue(schema.hasTable(new TableName("USERS")));
        assertFalse(schema.hasTable(new TableName("ORDERS")));
    }

    @Test
    void getTotalColumnCount_ReturnsCorrectCount() {
        Table usersTable = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null),
                        new Column(new ColumnName("NAME"), DataType.VARCHAR2, true, 2, null)
                ))
                .build();

        Table ordersTable = Table.builder()
                .name(new TableName("ORDERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null),
                        new Column(new ColumnName("USER_ID"), DataType.NUMBER, false, 2, null),
                        new Column(new ColumnName("TOTAL"), DataType.NUMBER, true, 3, null)
                ))
                .build();

        SchemaMetadata schema = SchemaMetadata.builder()
                .ownerId("user123")
                .tables(List.of(usersTable, ordersTable))
                .build();

        assertEquals(5, schema.getTotalColumnCount());
    }

    @Test
    void getAllForeignKeys_ReturnsAllFKs() {
        Table usersTable = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null)))
                .build();

        ForeignKey fk = ForeignKey.builder()
                .name(new ConstraintName("FK_orders_user"))
                .addSourceColumn(new ColumnName("USER_ID"))
                .targetTable(new TableName("USERS"))
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

        SchemaMetadata schema = SchemaMetadata.builder()
                .ownerId("user123")
                .tables(List.of(usersTable, ordersTable))
                .build();

        assertEquals(1, schema.getAllForeignKeys().size());
    }

    @Test
    void getTablesReferencing_ReturnsReferencingTables() {
        Table usersTable = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null)))
                .build();

        TableName usersTableName = usersTable.getName();

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

        SchemaMetadata schema = SchemaMetadata.builder()
                .ownerId("user123")
                .tables(List.of(usersTable, ordersTable))
                .build();

        List<Table> referencing = schema.getTablesReferencing(usersTableName);

        assertEquals(1, referencing.size());
        assertEquals("ORDERS", referencing.get(0).getName().value());
    }

    @Test
    void withTables_ReturnsNewSchemaWithNewTables() {
        Table usersTable = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null)))
                .build();

        SchemaMetadata original = SchemaMetadata.builder()
                .ownerId("user123")
                .tables(List.of(usersTable))
                .build();

        Table newTable = Table.builder()
                .name(new TableName("NEW_TABLE"))
                .columns(List.of(new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null)))
                .build();

        SchemaMetadata updated = original.withTables(List.of(newTable));

        assertEquals(1, updated.getTableCount());
        assertTrue(updated.hasTable(new TableName("NEW_TABLE")));
    }
}
