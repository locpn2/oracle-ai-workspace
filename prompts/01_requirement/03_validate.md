# Requirement Validation - Kiểm tra Yêu cầu

## Mục tiêu
Validate requirements đảm bảo đầy đủ, khả thi, và có thể test được.

## Input → Output
- **Input:** SPEC.md từ `02_refine.md`
- **Output:** Validated requirements + sign-off

## Parallel Triggers
- Phụ thuộc `02_refine.md`

## Quality Gates
- [ ] Tất cả features có acceptance criteria
- [ ] Không có ambiguous requirements
- [ ] Stakeholders đã approve

## Key Questions
- Requirements có đủ detail để implement?
- Có conflicting requirements?
- Scope có phù hợp với timeline?

---

## Workflow

### Bước 1: Completeness Check
- [ ] Tất cả user stories có acceptance criteria
- [ ] Tất cả NFRs có measurable targets
- [ ] Edge cases đã được cover

### Bước 2: Feasibility Review
- [ ] Technical feasibility
- [ ] Resource feasibility
- [ ] Timeline feasibility

### Bước 3: Clarity Check
- [ ] Không có ambiguous terms
- [ ] Stakeholders hiểu đúng requirements
- [ ] Acceptance criteria có thể verify được

### Bước 4: Sign-off
- Stakeholder approval
- Tech lead approval

---

## Output Format

```markdown
# Validation Report - [Project Name]

## 1. Completeness
| Requirement | Status | Gap |
|-------------|--------|-----|
| ... | OK/MISSING | ... |

## 2. Feasibility
| Aspect | Assessment | Risk |
|--------|------------|------|
| Technical | ... | Low/Medium/High |

## 3. Clarifications Needed
| Item | Question | Answer |
|------|----------|--------|
| ... | ... | ... |

## 4. Sign-off
- [ ] Stakeholder: [Name] - [Date]
- [ ] Tech Lead: [Name] - [Date]

## 5. Ready for Design
- [ ] YES - Proceed to Phase 2
- [ ] NO - Back to Refinement
```
