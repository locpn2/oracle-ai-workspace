# Integration Tests - Kiểm thử Tích hợp

## Mục tiêu
Viết integration tests cho API, database, external services.

## Input → Output
- **Input:** Controllers, Repository implementations
- **Output:** Integration tests

## Parallel Triggers
- Phụ thuộc `04_testing/02_unit.md`

## Quality Gates
- [ ] Testcontainers cho DB
- [ ] Mocks cho external services
- [ ] Clean test data

## Key Questions
- Integration points cần test?
- Test data setup strategy?
- Parallel test execution?

---

## Workflow

### Bước 1: Testcontainers Setup
```java
@containers
class [IntegrationTest] {
    
    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:15")
        .withDatabaseName("test")
        .withUsername("test")
        .withPassword("test");
}
```

### Bước 2: Controller Tests
```java
@WebMvcTest([Controller].class)
class [Controller]IntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void shouldReturn200_whenValidRequest() throws Exception {
        mockMvc.perform(get("/api/[resource]"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$").isArray());
    }
}
```

### Bước 3: Repository Tests
```java
@DataJpaTest
class [Repository]IntegrationTest {
    
    @Autowired
    private [Repository] repository;
    
    @Test
    void shouldFindById() {
        Optional<Entity> result = repository.findById(id);
        assertThat(result).isPresent();
    }
}
```

---

## Output Format

```markdown
# Integration Tests - [Context Name]

## 1. Test Configuration
- Database: Testcontainers PostgreSQL
- Mock: MockServer cho external APIs

## 2. API Tests
| Endpoint | Method | Test |
|----------|--------|-----|
| /api/[resource] | GET | shouldReturn200 |

## 3. Repository Tests
| Method | Test | Expected |
|--------|------|----------|
| findById | shouldReturnEntity | isPresent |

## 4. CI Integration
```yaml
test:
  services:
    - postgres:15
```
```
