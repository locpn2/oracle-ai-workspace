# CI/CD Pipeline - Tích hợp Liên tục

## Mục tiêu
Thiết lập CI/CD pipeline với quality gates.

## Input → Output
- **Input:** Docker configs, test configs
- **Output:** GitHub Actions workflows

## Parallel Triggers
- Phụ thuộc `05_deployment/01_docker.md`

## Quality Gates
- [ ] Build pass
- [ ] Tests pass
- [ ] Security scan pass
- [ ] Image push success

## Key Questions
- Deployment target?
- Environment strategy?
- Rollback strategy?

---

## Workflow

### Bước 1: CI Pipeline
```yaml
name: CI
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build
        run: ./mvnw clean package -DskipTests
      
      - name: Test
        run: ./mvnw test
      
      - name: SonarQube
        run: ./mvnw sonar:sonar
      
      - name: Security Scan
        run: ./mvnw dependency:analyze
```

### Bước 2: CD Pipeline
```yaml
name: CD
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build & Push Image
        run: |
          docker build -t app:${{ github.sha }} .
          docker push registry/app:${{ github.sha }}
      
      - name: Deploy
        run: kubectl apply -f k8s/
```

### Bước 3: Environment Promotion
```
main → staging → production
```

---

## Output Format

```markdown
# CI/CD Pipeline - [Project Name]

## 1. CI Workflow
```yaml
[GitHub Actions content]
```

## 2. CD Workflow
```yaml
[GitHub Actions content]
```

## 3. Environments
| Environment | Branch | URL |
|-------------|--------|-----|
| Dev | develop | dev.example.com |
| Staging | staging | staging.example.com |
| Prod | main | example.com |

## 4. Quality Gates
- [ ] Unit tests > 70%
- [ ] No critical vulnerabilities
- [ ] Image size < 500MB
- [ ] Health check pass
```
