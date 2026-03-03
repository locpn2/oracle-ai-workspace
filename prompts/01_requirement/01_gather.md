# Requirement Gathering - Thu thập Yêu cầu

## Mục tiêu
Thu thập yêu cầu ban đầu từ stakeholder, xác định scope và mục tiêu dự án.

## Input → Output
- **Input:** Raw user requirements, project idea
- **Output:** Initial requirements document

## Parallel Triggers
- Có thể chạy song song với `02_design/01_event-storming.md` nếu domain đã rõ

## Quality Gates
- [ ] Đã xác định được actors chính
- [ ] Đã xác định được core features
- [ ] Đã xác định được constraints (time, budget, tech)

## Key Questions
- Dự án này giải quyết vấn đề gì?
- Ai là người dùng cuối?
- Dự án cần hoàn thành khi nào?

---

## Workflow

### Bước 1: Kickoff Meeting
Thu thập thông tin ban đầu:
- Project vision
- Business goals
- Stakeholders
- Constraints

### Bước 2: User Stories Discovery
Liệt kê các user stories tiềm năng:
```
As a [user type]
I want to [action]
So that [benefit]
```

### Bước 3: Scope Definition
Xác định:
- In-scope features
- Out-of-scope features
- Assumptions
- Dependencies

---

## Output Format

```markdown
# Project Name: [Tên]

## 1. Vision
[Mô tả ngắn gọn về dự án]

## 2. Goals
- [Goal 1]
- [Goal 2]

## 3. Stakeholders
| Stakeholder | Role | Interest |
|-------------|------|----------|
| ... | ... | ... |

## 4. Initial User Stories
| ID | Story | Priority |
|----|-------|----------|
| US01 | As a..., I want to..., So that... | P0 |

## 5. Constraints
- [Constraint 1]
- [Constraint 2]

## 6. Questions for Refinement
- [Question 1]
```
