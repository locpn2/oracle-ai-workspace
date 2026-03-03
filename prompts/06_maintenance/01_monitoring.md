# Monitoring & Observability - Giám sát Hệ thống

## Mục tiêu
Thiết lập metrics, logging, và alerting.

## Input → Output
- **Input:** Architecture, SLI requirements
- **Output:** Monitoring setup

## Parallel Triggers
- Phụ thuộc `05_deployment/02_cicd.md`

## Quality Gates
- [ ] Metrics exposed
- [ ] Dashboards created
- [ ] Alerts configured

## Key Questions
- SLI/SLO targets?
- Alert thresholds?
- Retention policy?

---

## Workflow

### Bước 1: Metrics Definition
| Metric | Type | SLI | SLO |
|--------|------|-----|-----|
| Request latency | Histogram | p95 < 200ms | 99% |
| Error rate | Counter | < 1% | 99.9% |
| Availability | Gauge | > 99.9% | 99.95% |

### Bước 2: Prometheus Configuration
```yaml
- job_name: 'app'
  metrics_path: '/actuator/prometheus'
  static_configs:
    - targets: ['app:8080']
```

### Bước 3: Grafana Dashboard
- Application metrics
- Database metrics
- AI service metrics

---

## Output Format

```markdown
# Monitoring - [Project Name]

## 1. SLI/SLO
| Service | SLI | Target | Alert |
|---------|-----|--------|-------|
| API | Latency | < 200ms | > 500ms |
| API | Error rate | < 1% | > 5% |
| Database | Availability | 99.9% | < 99% |

## 2. Prometheus Metrics
| Metric | Type | Description |
|--------|------|-------------|
| http_requests_total | Counter | ... |
| http_request_duration | Histogram | ... |

## 3. Grafana Dashboard
- [Dashboard JSON]

## 4. Alert Rules
```yaml
[Prometheus alert config]
```
