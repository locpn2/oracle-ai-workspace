# Containerization - Container hóa Ứng dụng

## Mục tiêu
Tạo Dockerfiles và docker-compose cho production.

## Input → Output
- **Input:** Application code
- **Output:** Docker configurations

## Parallel Triggers
- Phụ thuộc `04_testing/03_integration.md`

## Quality Gates
- [ ] Multi-stage builds
- [ ] Security best practices
- [ ] Optimized image size

## Key Questions
- Base images?
- Environment variables?
- Health checks?

---

## Workflow

### Bước 1: Backend Dockerfile
```dockerfile
# Build stage
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Runtime stage
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget --quiet --tries=1 --spider http://localhost:8080/actuator/health
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### Bước 2: Frontend Dockerfile
```dockerfile
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### Bước 3: docker-compose
```yaml
services:
  app:
    build: ./backend
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=prod
    depends_on:
      - postgres
      - oracle

  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: vector_store
    ports:
      - "5432:5432"
```

---

## Output Format

```markdown
# Containerization - [Project Name]

## 1. Backend Dockerfile
```dockerfile
[content]
```

## 2. Frontend Dockerfile
```dockerfile
[content]
```

## 3. docker-compose.yml
```yaml
[content]
```

## 4. Security Checklist
- [ ] Non-root user
- [ ] No secrets in image
- [ ] Health checks
- [ ] Resource limits
```
