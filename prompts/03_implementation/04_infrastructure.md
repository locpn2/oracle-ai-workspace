# Infrastructure Implementation - Triển khai Infrastructure

## Mục tiêu
Implement Repositories, Adapters, REST Controllers.

## Input → Output
- **Input:** Repository interfaces, API specs
- **Output:** Infrastructure code

## Parallel Triggers
- Phụ thuộc `03_implementation/03_application.md`

## Quality Gates
- [ ] Repository implementations implement interface
- [ ] Adapters wrap external services
- [ ] Controllers match API spec

## Key Questions
- JPA/ORM mapping strategy?
- External API integration?
- API versioning?

---

## Workflow

### Bước 1: JPA Entities
```java
@Entity
@Table(name = "[table_name]")
public class [EntityName]Entity {
    @Id
    @GeneratedValue
    private Long id;
    
    // Mappings to domain
}
```

### Bước 2: Repository Implementation
```java
@Repository
@RequiredArgsConstructor
public class [Name]RepositoryImpl implements [Interface] {
    private final JpaRepository jpaRepository;
    
    // Implementation
}
```

### Bước 3: REST Controllers
```java
@RestController
@RequestMapping("/api/[resource]")
@RequiredArgsConstructor
public class [Name]Controller {
    private final [Service] service;
    
    @GetMapping
    public ResponseEntity<List<Response>> list() { ... }
}
```

---

## Output Format

```markdown
# Infrastructure - [Context Name]

## 1. JPA Entities
### [Name]Entity.java
```java
// content
```

## 2. Repository Implementations
### [Name]RepositoryImpl.java
```java
// content
```

## 3. REST Controllers
### [Name]Controller.java
```java
// content
```

## 4. Adapters (if needed)
### [Name]Adapter.java
```java
// content
```

## 5. API Documentation
| Endpoint | Method | Description |
|----------|--------|-------------|
| ... | ... | ... |
```
