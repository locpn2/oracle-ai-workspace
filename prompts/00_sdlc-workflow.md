# AI SDLC Workflow - Tổng quan

## Mục tiêu
Xác định luồng làm việc tự động hóa toàn bộ SDLC với AI.

## Input → Output
- **Input:** User yêu cầu ban đầu
- **Output:** SDLC workflow hoàn chỉnh

## Parallel Triggers
- Tất cả phases có thể chạy song song theo dependency graph

## Quality Gates
- [ ] Mỗi phase phải hoàn thành checklist trước khi proceed
- [ ] Output của phase trước là input của phase sau

---

## Phase Overview

| Phase | Folder | Mô tả |
|-------|--------|-------|
| 1 | `01_requirement/` | Thu thập, tinh chỉnh, validation yêu cầu |
| 2 | `02_design/` | Event Storming, Strategic, Tactical Design |
| 3 | `03_implementation/` | Setup, Domain, Application, Infrastructure |
| 4 | `04_testing/` | Strategy, Unit Tests, Integration Tests |
| 5 | `05_deployment/` | Docker, CI/CD Pipeline |
| 6 | `06_maintenance/` | Monitoring, Runbooks |

---

## Parallel Workflow Graph

```
Phase 1 (Requirement)
        │
        ▼
┌───────┴───────┐
│               │
▼               ▼
Phase 2a    Phase 2b    Phase 2c
(Event)     (Strategic) (Tactical)
│               │           │
└───────┬───────┴───────┬───┘
        │               │
        ▼               ▼
    Phase 3a      Phase 3b
    (Setup)       (Domain)
        │           │
        └─────┬─────┘
              │
              ▼
        ┌─────┴─────┐
        ▼           ▼
    Phase 3c   Phase 4a
    (App)      (Testing)
        │           │
        └─────┬─────┘
              │
              ▼
        ┌─────┴─────┐
        ▼           ▼
    Phase 5     Phase 6
    (Deploy)    (Maintain)
```

---

## Navigation

| Khi cần | Xem |
|---------|-----|
| Thu thập yêu cầu mới | `01_requirement/01_gather.md` |
| Tinh chỉnh yêu cầu | `01_requirement/02_refine.md` |
| Validate requirements | `01_requirement/03_validate.md` |
| Event Storming | `02_design/01_event-storming.md` |
| Strategic Design | `02_design/02_strategic.md` |
| Tactical Design | `02_design/03_tactical.md` |
| Setup project | `03_implementation/01_setup.md` |
| Implement Domain | `03_implementation/02_domain.md` |
| Implement Application | `03_implementation/03_application.md` |
| Implement Infrastructure | `03_implementation/04_infrastructure.md` |
| Test Strategy | `04_testing/01_strategy.md` |
| Unit Tests | `04_testing/02_unit.md` |
| Integration Tests | `04_testing/03_integration.md` |
| Docker | `05_deployment/01_docker.md` |
| CI/CD | `05_deployment/02_cicd.md` |
| Monitoring | `06_maintenance/01_monitoring.md` |
| Runbooks | `06_maintenance/02_runbooks.md` |

---

## Quality Gate Checklist (mỗi phase)

- [ ] Input từ phase trước đã được review
- [ ] Output đã meet quality standards
- [ ] Documentation đã update
- [ ] Questions đã được trả lời trước khi proceed
