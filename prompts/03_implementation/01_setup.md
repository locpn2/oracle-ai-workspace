# Infrastructure Setup - Thiết lập Hạ tầng

## Mục tiêu
Thiết lập project structure, dependencies, và configuration.

## Input → Output
- **Input:** SPEC.md, Tech stack requirements
- **Output:** Project scaffolding, docker-compose, configs

## Parallel Triggers
- Phụ thuộc `02_design/03_tactical.md`

## Quality Gates
- [ ] Project structure theo architecture đã chọn
- [ ] Dependencies đã verified
- [ ] Docker compose chạy được

## Key Questions
- Architecture pattern (Layered/Hexagonal/Clean)?
- Multi-module hay single module?
- Database connections?

---

## Workflow

### Bước 1: Project Scaffolding
```
src/
├── main/
│   ├── java/
│   │   └── [package]/
│   │       ├── domain/
│   │       │   ├── entity/
│   │       │   ├── valueobject/
│   │       │   ├── repository/
│   │       │   └── service/
│   │       ├── application/
│   │       │   ├── dto/
│   │       │   └── usecase/
│   │       ├── infrastructure/
│   │       │   ├── repository/
│   │       │   └── adapter/
│   │       └── api/
│   │           └── controller/
│   └── resources/
│       ├── application.yml
│       └── db/migration/
└── test/
```

### Bước 2: Dependencies Setup
- Maven/Gradle dependencies
- Spring Boot version
- Database drivers
- AI SDKs

### Bước 3: Docker Configuration
- docker-compose.yml
- Database services
- Cache services

---

## Output Format

```markdown
# Infrastructure Setup - [Project Name]

## 1. Project Structure
```
[folder tree]
```

## 2. Dependencies (pom.xml/build.gradle)
| Dependency | Version | Purpose |
|------------|---------|---------|
| ... | ... | ... |

## 3. Configuration
### application.yml
```yaml
[config]
```

## 4. Docker Services
| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| ... | ... | ... | ... |

## 5. Verification
- [ ] Build success
- [ ] Docker compose up
- [ ] Database connection OK
```
