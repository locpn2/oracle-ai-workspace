# AGENTS.md - AI SDLC Workflow Guidelines

## 1. Project Overview

This is an **AI SDLC Workflow System** - a documentation and prompt-based framework for guiding AI agents to execute full software development lifecycle. The system transforms user requirements into complete software implementations through 6 sequential phases.

**Input:** `docs/requirement.md` (user's initial request)
**Output:** Complete software implementation in `docs/artifacts/`

---

## 2. Directory Structure

```
oracle-ai-workspace/
├── docs/
│   ├── requirement.md        # INPUT: Initial user requirements
│   └── artifacts/           # OUTPUT: Generated artifacts per phase
│       ├── phase1_requirement/
│       │   ├── SPEC.md
│       │   └── validation-report.md
│       ├── phase2_design/
│       │   ├── event-storming.md
│       │   ├── context-map.md
│       │   └── domain-model.md
│       ├── phase3_implementation/
│       ├── phase4_testing/
│       ├── phase5_deployment/
│       └── phase6_maintenance/
├── prompts/                  # AI Agent prompts (DO NOT modify)
│   ├── 00_sdlc-workflow.md
│   ├── 01_requirement/      # Phase 1: 3 prompts
│   ├── 02_design/           # Phase 2: 3 prompts
│   ├── 03_implementation/   # Phase 3: 4 prompts
│   ├── 04_testing/          # Phase 4: 3 prompts
│   ├── 05_deployment/       # Phase 5: 2 prompts
│   └── 06_maintenance/      # Phase 6: 2 prompts
└── .gitignore
```

---

## 3. AI Workflow Execution

### 3.1 Multi-Agent Architecture

Each phase is handled by a specialized agent:

| Agent | Phase | Prompts |
|-------|-------|---------|
| Requirement Agent | Phase 1 | gather → refine → validate |
| Design Agent | Phase 2 | event-storming → strategic → tactical |
| Implementation Agent | Phase 3 | setup → domain → application → infrastructure |
| Testing Agent | Phase 4 | strategy → unit → integration |
| Deployment Agent | Phase 5 | docker → cicd |
| Maintenance Agent | Phase 6 | monitoring → runbooks |

### 3.2 Hybrid Phase Detection

**Step 1: Analyze artifacts directory**
```python
def detect_next_phase(artifacts_dir):
    if not exists(artifacts_dir / "phase1_requirement" / "SPEC.md"):
        return "Phase 1: Requirement"
    elif not exists(artifacts_dir / "phase2_design" / "context-map.md"):
        return "Phase 2: Design"
    elif not exists(artifacts_dir / "phase3_implementation" / "domain"):
        return "Phase 3: Implementation"
    # ... continue
    return "All phases completed"
```

**Step 2: Confirm with user**
```
I detected Phase 1 is not complete. Proceed with Requirement Gathering?
[Y] Yes - Start Phase 1
[N] No - Wait for explicit phase specification
[1-6] Specify phase number explicitly
```

### 3.3 Execution Flow

```
User Input: docs/requirement.md
        ↓
Agent detects: New project → Phase 1
        ↓
User confirms: Y
        ↓
Execute Phase 1 prompts sequentially:
  01_gather.md → Quality Gates → Output artifacts
  02_refine.md → Quality Gates → Output artifacts
  03_validate.md → Quality Gates → SPEC.md
        ↓
Detect next phase: Phase 2
        ↓
[Repeat until all phases complete]
```

---

## 4. Build/Lint/Test Commands

When code is generated, use the following commands:

### 4.1 Java/Spring Boot (Primary)

```bash
# Build
./mvnw clean package -DskipTests

# Run single test class
./mvnw test -Dtest=UserServiceTest

# Run single test method
./mvnw test -Dtest=UserServiceTest#shouldCreateUser_whenValidInput

# Lint (if available)
./mvnw checkstyle:check

# Code format
./mvnw formatter:format
```

### 4.2 General

```bash
# Install dependencies
npm install  # Node.js
pip install -r requirements.txt  # Python

# Run tests
npm test
pytest tests/

# Lint
npm run lint
ruff check .
```

---

## 5. Code Style Guidelines

### 5.1 Domain-Driven Design Patterns

**Layer Structure:**
```
src/main/java/[package]/
├── domain/
│   ├── entity/           # JPA entities (DB mapping)
│   ├── model/            # Domain models (business logic)
│   ├── valueobject/      # Immutable value objects
│   ├── aggregate/        # Aggregate roots
│   ├── repository/       # Repository interfaces
│   └── service/          # Domain services
├── application/
│   ├── dto/              # Request/Response DTOs
│   ├── usecase/          # Use case implementations
│   └── service/          # Application services
├── infrastructure/
│   ├── persistence/     # JPA repositories
│   ├── adapter/          # External service adapters
│   └── config/           # Configuration
└── api/
    └── controller/       # REST controllers
```

### 5.2 Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Class | PascalCase | `UserService`, `OrderAggregate` |
| Method | camelCase | `createUser()`, `findById()` |
| Variable | camelCase | `userName`, `orderList` |
| Constant | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Package | lowercase | `com.example.domain` |
| Test Class | `*Test` | `UserServiceTest` |
| Test Method | `should_*_when_*` | `shouldCreateUser_whenValidInput` |

### 5.3 Test Conventions

**Naming:** `should_[expected]_when_[condition]`

```java
@Test
void shouldCreateUser_whenValidInput() { }

@Test
void shouldThrowException_whenEmailInvalid() { }
```

**Structure (Given/When/Then):**
```java
@Test
void shouldCreateUser_whenValidInput() {
    // Given
    UserInput input = new UserInput("John", "john@example.com");
    
    // When
    User result = userService.create(input);
    
    // Then
    assertThat(result.getName()).isEqualTo("John");
}
```

### 5.4 Error Handling

- Use domain exceptions for business logic errors
- Use `IllegalArgumentException` for validation errors
- Use `RuntimeException` for unexpected errors
- Always include meaningful error messages

---

## 6. Git Commit Rules

### 6.1 Format

```
<type>(scope): <short description>

[body(s)]

[optional footer]
```

### 6.2 Allowed Types

| Type | Description |
|------|-------------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `refactor` | Code changes that neither fix a bug nor add a feature |
| `chore` | Routine tasks, build process, or auxiliary tool changes |
| `docs` | Documentation updates |
| `style` | Code style changes (formatting, missing semicolons) |
| `test` | Adding or updating tests |

### 6.3 Example

```
250409@locpn: feat(api): add customer search endpoint

This commit introduces a new endpoint `/api/customers/search` that allows 
filtering by name and email. Pagination is also supported.

BREAKING CHANGE: the old `/api/customers/find` endpoint is removed
```

### 6.4 Rules

- Write commit messages in **Vietnamese** (preferred) or English
- Add `BREAKING CHANGE:` in footer when introducing incompatible changes
- Avoid vague messages: `commit`, `update code`, `fix something`, `change`

---

## 7. Quality Gates

**Every phase MUST pass all checklist items before proceeding.**

### Phase 1: Requirement
- [ ] Actors chính đã xác định
- [ ] Core features đã xác định
- [ ] Constraints đã xác định
- [ ] Features có use case rõ ràng
- [ ] NFRs đã được xác định
- [ ] Tất cả features có acceptance criteria
- [ ] Stakeholders đã approve

### Phase 2: Design
- [ ] Đủ events cho core features
- [ ] Commands và events có flow hợp lý
- [ ] Mỗi context có clear responsibility
- [ ] Relationships giữa contexts đã xác định
- [ ] Mỗi aggregate có clear invariant

### Phase 3: Implementation
- [ ] Project structure theo architecture
- [ ] Dependencies đã verified
- [ ] Docker compose chạy được
- [ ] Invariants được enforce trong code
- [ ] Value Objects là immutable

### Phase 4: Testing
- [ ] Coverage targets realistic
- [ ] Test types phân bổ hợp lý (Unit 70%, Integration 20%, E2E 10%)
- [ ] Invariants tested
- [ ] Edge cases covered
- [ ] Tests are isolated

### Phase 5: Deployment
- [ ] Multi-stage builds
- [ ] Security best practices
- [ ] Optimized image size
- [ ] Build pass
- [ ] Tests pass

---

## 8. Phase Navigation Quick Reference

| Phase | When to Use | Key Artifacts |
|-------|-------------|---------------|
| **Phase 1** | New project, unclear requirements | SPEC.md, use-cases.md |
| **Phase 2** | Need domain design | context-map.md, domain-model.md |
| **Phase 3** | Ready to code | domain/, application/, infrastructure/ |
| **Phase 4** | Need tests | unit-tests/, integration-tests/ |
| **Phase 5** | Ready to deploy | Dockerfile, docker-compose.yml, CI/CD |
| **Phase 6** | Production ready | monitoring/, runbooks/ |

---

## Quick Start

```bash
# 1. Read initial requirements
cat docs/requirement.md

# 2. Agent detects: New project → Phase 1
# 3. Confirm: Y

# 4. Phase 1 executes:
#    - 01_gather.md → Creates initial docs
#    - 02_refine.md → Creates SPEC.md
#    - 03_validate.md → Validates and signs off

# 5. Detect next phase → Phase 2...
```
