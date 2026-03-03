# Unit Tests - Kiểm thử Đơn vị

## Mục tiêu
Viết unit tests cho domain logic, enforce invariants.

## Input → Output
- **Input:** Domain layer code
- **Output:** Unit tests

## Parallel Triggers
- Phụ thuộc `04_testing/01_strategy.md`

## Quality Gates
- [ ] Invariants tested
- [ ] Edge cases covered
- [ ] Tests are isolated

## Key Questions
- Test Happy path và sad path?
- Mock dependencies?
- Test naming convention?

---

## Workflow

### Bước 1: Aggregate Tests
```java
@ExtendWith(MockitoExtension.class)
class [AggregateName]Test {
    
    @Test
    void should_[behavior]_when_[condition]() {
        // Given
        [Aggregate] aggregate = ...
        
        // When
        aggregate.[action]();
        
        // Then
        assertThat(aggregate.[state]()).isEqualTo(...);
    }
    
    @Test
    void shouldThrow_[Exception]_when_[condition]() {
        // Then
        assertThatThrownBy(() -> aggregate.[action]())
            .isInstanceOf(DomainException.class);
    }
}
```

### Bước 2: Value Object Tests
```java
@Test
void shouldThrowException_whenInvalidValue() {
    assertThatThrownBy(() -> new VO(null))
        .isInstanceOf(IllegalArgumentException.class);
}
```

### Bước 3: Use Case Tests
```java
@Test
void should_[expected]_when_[input]() {
    // Given
    when(repository.findById(id)).thenReturn(Optional.of(entity));
    
    // When
    Output result = useCase.execute(input);
    
    // Then
    assertThat(result).isNotNull();
}
```

---

## Output Format

```markdown
# Unit Tests - [Context Name]

## 1. Test Structure
```
test/
├── domain/
│   ├── [AggregateName]Test.java
│   └── [ValueObject]Test.java
└── application/
    └── [UseCaseName]Test.java
```

## 2. Coverage Report
| Class | Coverage |
|-------|----------|
| [AggregateName] | XX% |

## 3. Key Test Cases
| Test | Type | Description |
|------|------|-------------|
| shouldCreate_whenValid | Happy | ... |
| shouldThrow_whenInvalid | Sad | ... |
```
