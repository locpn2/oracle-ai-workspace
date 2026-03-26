# Tech Context - VecBase

## Công nghệ sử dụng

### Backend Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Java | 21 | Main language |
| Spring Boot | 3.2.x | Application framework |
| Spring Security | 6.x | Authentication/Authorization |
| Spring Data JPA | 3.x | Data access layer |
| Oracle JDBC | 21.x | Oracle database driver |
| Lombok | 1.18.x | Boilerplate reduction |
| MapStruct | 1.5.x | Object mapping |

### Frontend Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.x | UI framework |
| TypeScript | 5.x | Type safety |
| Redux Toolkit | 2.x | State management |
| React Flow | 11.x | ERD visualization |
| Ant Design | 5.x | UI components |
| Axios | 1.x | HTTP client |

### AI/ML Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| LangChain | 0.1.x | LLM orchestration |
| OpenAI API | Latest | GPT-4 for text-to-SQL |
| Sentence Transformers | 2.x | Text embeddings |
| HuggingFace | Latest | Model hub |

### Vector Database
| Technology | Version | Purpose |
|------------|---------|---------|
| PostgreSQL + pgvector | 15+ | Vector storage |
| Redis Stack | 7.x | Vector cache (optional) |

### Infrastructure
| Technology | Version | Purpose |
|------------|---------|---------|
| Docker | 24.x | Containerization |
| Docker Compose | 2.x | Multi-container orchestration |
| Nginx | 1.25.x | Reverse proxy |
| Prometheus | 2.x | Metrics collection |
| Grafana | 10.x | Monitoring dashboard |

## Development Setup

### Prerequisites
```bash
# Required software
- JDK 21+
- Node.js 20+
- Docker Desktop
- Oracle Database (or Oracle XE for dev)
- PostgreSQL 15+ with pgvector
```

### Local Development
```bash
# Backend
cd backend
./mvnw spring-boot:run -Dspring-boot.run.profiles=local

# Frontend
cd frontend
npm install
npm run dev

# Infrastructure
docker-compose up -d
```

### Environment Variables
```bash
# Database
ORACLE_URL=jdbc:oracle:thin:@localhost:1521:XE
ORACLE_USERNAME=vecbase
ORACLE_PASSWORD=secret

# Vector DB
PGVECTOR_URL=jdbc:postgresql://localhost:5432/vecbase_vectors
PGVECTOR_USERNAME=vecbase
PGVECTOR_PASSWORD=secret

# AI
OPENAI_API_KEY=sk-xxx
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Technical Constraints

### Performance Requirements
| Metric | Target | Measurement |
|--------|--------|-------------|
| Schema load time | < 2s | Time to render ERD |
| Query response time | < 5s | End-to-end AI query |
| Vector conversion | < 10min | 100 tables |
| Concurrent users | 50+ | Simultaneous sessions |

### Scalability Constraints
- **Database connections**: Max 20 concurrent Oracle connections
- **Memory**: 4GB heap for backend service
- **Storage**: Vector embeddings ~1KB per row average
- **API rate limit**: 100 requests/minute/user

### Security Requirements
- **Authentication**: JWT with refresh tokens
- **Authorization**: Role-based (Admin, User, Viewer)
- **Encryption**: TLS 1.3 for all connections
- **Audit**: Log all data access and modifications

### Compatibility
- **Oracle versions**: 12c, 18c, 19c, 21c
- **Browsers**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **OS**: Windows 10+, macOS 12+, Ubuntu 20.04+

## Architecture Decisions

### Why Spring Boot?
- Mature ecosystem for enterprise Java
- Excellent Oracle integration
- Strong security framework
- Large community support

### Why React?
- Component-based architecture
- Rich ecosystem for visualization
- TypeScript support
- Performance with virtual DOM

### Why PostgreSQL + pgvector?
- Open source and cost-effective
- pgvector extension for vector operations
- Good performance for moderate scale
- Easy integration with Spring Data

### Why LangChain?
- Abstraction over multiple LLM providers
- Built-in chains for SQL generation
- Extensible with custom tools
- Active development and community

## Dependencies Management

### Backend (Maven)
```xml
<properties>
    <java.version>21</java.version>
    <spring-boot.version>3.2.0</spring-boot.version>
</properties>
```

### Frontend (npm)
```json
{
  "engines": {
    "node": ">=20.0.0"
  }
}
```

## Build & Deploy

### Build Commands
```bash
# Backend
./mvnw clean package -DskipTests

# Frontend
npm run build

# Docker
docker-compose build
```

### CI/CD Pipeline
1. Code push → GitHub Actions
2. Run tests (unit + integration)
3. Build Docker images
4. Push to registry
5. Deploy to staging
6. Run E2E tests
7. Deploy to production