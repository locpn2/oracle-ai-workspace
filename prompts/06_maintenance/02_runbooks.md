# Incident Response Runbooks - Sổ tay Sự cố

## Mục tiêu
Tạo runbooks cho các sự cố phổ biến.

## Input → Output
- **Input:** System architecture, known failure modes
- **Output:** Runbook documents

## Parallel Triggers
- Phụ thuộc `06_maintenance/01_monitoring.md`

## Quality Gates
- [ ] Runbooks cho critical incidents
- [ ] Escalation procedures
- [ ] Post-mortem template

## Key Questions
- Common failure scenarios?
- On-call rotation?
- Communication plan?

---

## Workflow

### Bước 1: Incident Classification
| Severity | Response Time | Example |
|----------|---------------|---------|
| SEV1 | < 15 min | Complete outage |
| SEV2 | < 1 hour | Partial outage |
| SEV3 | < 4 hours | Degraded performance |

### Bước 2: Runbook Template
```markdown
# [Incident Name]

## Symptoms
- [Symptom 1]
- [Symptom 2]

## Impact
[Description]

## Diagnosis
1. [Step 1]
2. [Step 2]

## Resolution
1. [Step 1]
2. [Step 2]

## Escalation
- Contact: [Name/Role]
```

### Bước 3: Post-Mortem Template
```markdown
# Post-Mortem - [Incident]

## Summary
## Timeline
## Root Cause
## Action Items
```

---

## Output Format

```markdown
# Runbooks - [Project Name]

## 1. Incident Classification
| Severity | Response | Examples |
|----------|----------|----------|
| SEV1 | 15 min | ... |
| SEV2 | 1 hour | ... |

## 2. Runbooks
### RB-001: Database Connection Failure
[Content]

### RB-002: High CPU Usage
[Content]

## 3. Escalation Path
| Level | Contact | Response |
|-------|---------|----------|
| L1 | On-call | 15 min |
| L2 | Tech Lead | 1 hour |
| L3 | Manager | 4 hours |

## 4. Post-Mortem Template
[Template]
```
