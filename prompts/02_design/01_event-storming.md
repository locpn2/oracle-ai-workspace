# Event Storming - Khám phá Domain Events

## Mục tiêu
Xác định domain events, commands, và actors thông qua interactive session.

## Input → Output
- **Input:** Validated SPEC.md
- **Output:** Event storming artifacts

## Parallel Triggers
- Phụ thuộc `01_requirement/03_validate.md`
- Có thể chạy song song với `02_strategic.md`

## Quality Gates
- [ ] Đã xác định đủ events cho core features
- [ ] Commands và events có flow hợp lý
- [ ] Actors đã được xác định

## Key Questions
- Những sự kiện nào xảy ra trong hệ thống?
- Ai tạo ra events?
- Events có business meaning?

---

## Workflow

### Bước 1: Domain Discovery
Liệt kê:
- **Domain Events** (Cam): Điều gì xảy ra trong business
- **Commands** (Xanh): Hành động người dùng/hệ thống
- **Actors** (Vàng): Người/hệ thống thực hiện

### Bước 2: Timeline Flow
Sắp xếp events theo timeline:
```
User Login → System Authenticate → Session Created → ...
```

### Bước 3: Aggregation
Nhóm events theo business process

---

## Output Format

```markdown
# Event Storming - [Project Name]

## 1. Actors
| Actor | Type | Description |
|-------|------|-------------|
| ... | User/System | ... |

## 2. Commands
| Command | Actor | Trigger |
|---------|-------|---------|
| ... | ... | ... |

## 3. Domain Events
| Event | Type | Cause | Effect |
|-------|------|-------|--------|
| ... | ... | ... | ... |

## 4. Process Flows
### Flow 1: [Tên]
Command → Event → Event → ...
```
