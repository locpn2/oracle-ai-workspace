# Requirement Refinement - Tinh chỉnh Yêu cầu

## Mục tiêu
Tinh chỉnh yêu cầu thành SPEC chi tiết với use cases, NFRs, và acceptance criteria.

## Input → Output
- **Input:** Raw requirements từ `01_gather.md`
- **Output:** Detailed SPEC.md

## Parallel Triggers
- Phụ thuộc `01_gather.md` - chạy sau khi gather hoàn thành

## Quality Gates
- [ ] Mỗi feature có use case rõ ràng
- [ ] NFRs đã được xác định
- [ ] Questions từ gather đã được trả lời

## Key Questions
- Chi tiết kỹ thuật của từng feature?
- Performance requirements?
- Security requirements?

---

## Workflow

### Bước 1: Feature Decomposition
Phân rã features thành:
- Functional requirements
- Non-functional requirements (NFRs)
- Technical constraints

### Bước 2: Use Case Development
Mỗi feature cần:
```
UC-[ID]: [Tên Use Case]
Actor: [Ai thực hiện]
Pre-condition: [Điều kiện trước]
Flow:
  1. [Bước 1]
  2. [Bước 2]
Post-condition: [Điều kiện sau]
```

### Bước 3: Acceptance Criteria
Cho mỗi user story:
```
AC-[ID]: [Mô tả]
- [ ] Criterion 1
- [ ] Criterion 2
```

---

## Output Format

```markdown
# SPEC.md - [Project Name]

## 1. Functional Requirements
| ID | Requirement | Priority | Use Case |
|----|-------------|----------|----------|
| FR01 | ... | P0 | UC01 |

## 2. Non-Functional Requirements
| Category | Requirement | Target |
|----------|-------------|--------|
| Performance | ... | ... |
| Security | ... | ... |
| Scalability | ... | ... |

## 3. Use Cases
### UC-[ID]: [Tên]
...

## 4. Acceptance Criteria
### AC-[ID]: [Tên]
- [ ] ...

## 5. Tech Stack Selection
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Backend | ... | ... |
| Frontend | ... | ... |
| Database | ... | ... |
```
