package com.oracleai.workspace.schema.application;

import com.oracleai.workspace.schema.application.service.SchemaApplicationService;
import com.oracleai.workspace.schema.domain.entity.SchemaMetadata;
import com.oracleai.workspace.schema.domain.entity.Table;
import com.oracleai.workspace.schema.domain.valueobject.*;
import com.oracleai.workspace.schema.application.port.out.SchemaRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class SchemaApplicationServiceTest {

    @Mock
    private SchemaRepository schemaRepository;

    private SchemaApplicationService schemaService;

    @BeforeEach
    void setUp() {
        schemaService = new SchemaApplicationService(schemaRepository);
    }

    @Test
    void extractSchema_WithValidUser_ReturnsSchema() {
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

        doReturn(schema).when(schemaRepository).extractFromOracle("user123");
        doNothing().when(schemaRepository).save(any(SchemaMetadata.class));

        SchemaMetadata result = schemaService.extractSchema("user123");

        assertNotNull(result);
        assertEquals(1, result.getTableCount());
        verify(schemaRepository).extractFromOracle("user123");
        verify(schemaRepository).save(any(SchemaMetadata.class));
    }

    @Test
    void getSchema_WhenExists_ReturnsSchema() {
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

        doReturn(Optional.of(schema)).when(schemaRepository).findByOwnerId("user123");

        Optional<SchemaMetadata> result = schemaService.getSchema("user123");

        assertTrue(result.isPresent());
        assertEquals("user123", result.get().getOwnerId());
    }

    @Test
    void getSchema_WhenNotExists_ReturnsEmpty() {
        doReturn(Optional.empty()).when(schemaRepository).findByOwnerId("nonexistent");

        Optional<SchemaMetadata> result = schemaService.getSchema("nonexistent");

        assertTrue(result.isEmpty());
    }

    @Test
    void refreshSchema_WithValidUser_ReturnsUpdatedSchema() {
        Table usersTable = Table.builder()
                .name(new TableName("USERS"))
                .columns(List.of(
                        new Column(new ColumnName("ID"), DataType.NUMBER, false, 1, null),
                        new Column(new ColumnName("EMAIL"), DataType.VARCHAR2, true, 2, null)
                ))
                .build();

        SchemaMetadata schema = SchemaMetadata.builder()
                .ownerId("user123")
                .tables(List.of(usersTable))
                .build();

        doReturn(schema).when(schemaRepository).extractFromOracle("user123");
        doNothing().when(schemaRepository).save(any(SchemaMetadata.class));

        SchemaMetadata result = schemaService.refreshSchema("user123");

        assertNotNull(result);
        assertEquals(2, result.getTotalColumnCount());
        verify(schemaRepository).extractFromOracle("user123");
        verify(schemaRepository, times(1)).save(any(SchemaMetadata.class));
    }
}
