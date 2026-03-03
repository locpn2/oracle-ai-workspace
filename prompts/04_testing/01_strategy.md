# Test Strategy - Chiến lược Kiểm thử

## Mục tiêu
Xác định test pyramid, coverage targets, và test approach.

## Input → Output
- **Input:** Domain model, Use cases
- **Output:** Test strategy document

## Parallel Triggers
- Phụ thuộc `03_implementation/02_domain.md`

## Quality Gates
- [ ] Coverage targets realistic
- [ ] Test types phân bổ hợp lý
- [ ] Risk areas identified

## Key Questions
- Critical paths cần ưu tiên?
- Coverage requirements?
- Automated vs manual?

---

## Workflow

### Bước 1: Test Pyramid Design
```
        /\
       /  \      E2E (10%)
      /----\     Integration (20%)
     /      \    Unit (70%)
    /________\
```

### Bước 2: Coverage Targets
| Layer | Target | Focus |
|-------|--------|-------|
| Unit | 80% | Domain logic |
| Integration | 60% | API, DB |
| E2E | Critical paths | User flows |

### Bước 3: Test Tools Selection
- Unit: JUnit/Mockito
- Integration: Testcontainers
- E2E: Playwright/Cypress

---

## Output Format

```markdown
# Test Strategy - [Project Name]

## 1. Test Pyramid
| Layer | % | Tools |
|-------|---|-------|
| E2E | 10% | ... |
| Integration | 20% | ... |
| Unit | 70% | ... |

## 2. Coverage Targets
| Area | Target | Priority |
|------|--------|----------|
| Domain | 80% | High |
| Services | 70% | High |
| Controllers | 60% | Medium |

## 3. Test Environments
| Environment | Purpose | Data |
|-------------|---------|------|
| Dev | Local dev | Mock |
| Test | CI/CD | Testcontainers |
| Staging | Pre-prod | Sanitized |

## 4. Risk-based Testing
| Feature | Risk | Test Priority |
|---------|------|---------------|
| ... | ... | ... |
```
