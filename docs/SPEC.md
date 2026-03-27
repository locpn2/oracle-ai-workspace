# SPEC.md - VecBase

## 1. Vision

VecBase là công cụ trực quan hóa dữ liệu Oracle DB tích hợp AI-powered query và khả năng chuyển đổi RDBMS sang Vector DB, giúp mọi người (kể cả người không chuyên) có thể hiểu và tương tác với dữ liệu một cách dễ dàng.

## 2. Goals

### Business Goals
- **Democratize data access**: Cho phép non-technical users truy cập dữ liệu mà không cần SQL knowledge
- **Accelerate AI integration**: Giảm thời gian chuyển đổi RDBMS sang Vector DB từ tuần xuống giờ
- **Improve data understanding**: Giúp stakeholders hiểu cấu trúc database trong < 5 phút

### Technical Goals
- **High performance**: Schema load < 2s, Query response < 5s
- **High accuracy**: AI query accuracy > 90%
- **Scalability**: Support 50+ concurrent users

## 3. Stakeholders

| Stakeholder | Role | Interest | Priority |
|-------------|------|----------|----------|
| DBA | Database Administrator | Schema management, performance monitoring | High |
| Data Analyst | Người phân tích dữ liệu | Self-service data access, visualization | High |
| AI Engineer | Kỹ sư AI | Vector DB, embeddings, ML integration | High |
| Developer | Lập trình viên | API integration, automation | Medium |
| Project Sponsor | Người tài trợ | ROI, business value | High |

## 4. User Stories

### 4.1 Visualization Module

#### US-01: View Database Schema
**As a** Data Analyst  
**I want to** view the entire database schema in a visual ERD diagram  
**So that** I can quickly understand the data structure without reading documentation

**Acceptance Criteria:**
- [ ] ERD diagram displays all tables in selected schema
- [ ] Shows relationships (PK, FK) between tables
- [ ] Displays column names and data types
- [ ] Load time < 2 seconds for schemas with < 100 tables
- [ ] Zoom in/out and pan functionality

**Priority:** P0 (Must Have)

---

#### US-02: Browse Table Details
**As a** DBA  
**I want to** click on a table to view its detailed information  
**So that** I can review columns, constraints, indexes, and statistics

**Acceptance Criteria:**
- [ ] Click on table shows detail panel
- [ ] Display columns with data types, nullable, default values
- [ ] Show primary keys, foreign keys, unique constraints
- [ ] Display indexes and their types
- [ ] Show row count and table size

**Priority:** P0 (Must Have)

---

#### US-03: Export ERD
**As a** Developer  
**I want to** export the ERD diagram as PNG/SVG/PDF  
**So that** I can include it in documentation

**Acceptance Criteria:**
- [ ] Export to PNG format
- [ ] Export to SVG format
- [ ] Export to PDF format
- [ ] Maintain quality and readability

**Priority:** P2 (Nice to Have)

---

### 4.2 AI Query Module

#### US-04: Natural Language Query
**As a** Data Analyst  
**I want to** ask questions in natural language  
**So that** I can get data without writing SQL

**Acceptance Criteria:**
- [ ] Accept Vietnamese and English queries
- [ ] Generate SQL from natural language
- [ ] Display generated SQL for transparency
- [ ] Execute query and show results
- [ ] Query accuracy > 90%

**Priority:** P0 (Must Have)

**Example:**
```
Input: "Cho tôi xem danh sách nhân viên phòng IT"
Output: SELECT * FROM employees WHERE department = 'IT'
```

---

#### US-05: Query History
**As a** Data Analyst  
**I want to** view my query history  
**So that** I can reuse previous queries

**Acceptance Criteria:**
- [ ] Store last 100 queries per user
- [ ] Search query history
- [ ] Re-run previous queries
- [ ] Export query history to CSV and JSON formats

**Priority:** P1 (Should Have)

---

#### US-06: Query Suggestions
**As a** Data Analyst  
**I want to** receive query suggestions based on schema  
**So that** I can discover useful queries

**Acceptance Criteria:**
- [ ] Suggest queries based on table relationships
- [ ] Show popular queries
- [ ] Context-aware suggestions

**Priority:** P2 (Nice to Have)

---

### 4.3 Data Clustering Module

#### US-07: Auto-Cluster Tables
**As a** DBA  
**I want to** automatically group related tables  
**So that** I can organize data by business domains

**Acceptance Criteria:**
- [ ] Analyze table relationships
- [ ] Group tables by domain (HR, Finance, Sales, etc.)
- [ ] Allow manual adjustment of groups
- [ ] Save clustering configuration

**Priority:** P1 (Should Have)

---

#### US-08: View Cluster Details
**As a** Data Analyst  
**I want to** view tables grouped by cluster  
**So that** I can focus on specific business domains

**Acceptance Criteria:**
- [ ] Display clusters in sidebar
- [ ] Filter ERD by cluster
- [ ] Show cluster statistics
- [ ] Navigate between clusters

**Priority:** P1 (Should Have)

---

### 4.4 Vector Conversion Module

#### US-09: Convert Schema to Vector DB
**As an** AI Engineer  
**I want to** convert Oracle schema to Vector DB  
**So that** I can use it for AI/ML applications

**Acceptance Criteria:**
- [ ] Select tables for conversion
- [ ] Configure mapping rules
- [ ] Preview conversion result
- [ ] Execute conversion
- [ ] Track conversion progress

**Priority:** P0 (Must Have)

---

#### US-10: Generate Embeddings
**As an** AI Engineer  
**I want to** generate vector embeddings for text columns  
**So that** I can perform semantic search

**Acceptance Criteria:**
- [ ] Select text columns for embedding
- [ ] Choose embedding model
- [ ] Generate embeddings in batch
- [ ] Store in pgvector
- [ ] Verify embedding quality

**Priority:** P0 (Must Have)

---

#### US-11: Vector Search
**As an** AI Engineer  
**I want to** perform semantic search on vector data  
**So that** I can find similar records

**Acceptance Criteria:**
- [ ] Input search query
- [ ] Generate query embedding
- [ ] Find similar vectors
- [ ] Display results with similarity score
- [ ] Response time < 1 second

**Priority:** P1 (Should Have)

---

#### US-12: Conversion History
**As an** AI Engineer  
**I want to** view conversion history  
**So that** I can track and rollback changes

**Acceptance Criteria:**
- [ ] List all conversion jobs
- [ ] Show job status and progress
- [ ] View conversion details
- [ ] Rollback to previous version

**Priority:** P1 (Should Have)

---

### 4.5 Administration Module

#### US-13: Manage Database Connections
**As an** Admin  
**I want to** manage database connections  
**So that** users can connect to different databases

**Acceptance Criteria:**
- [ ] Add new connection
- [ ] Edit connection settings
- [ ] Test connection
- [ ] Delete connection
- [ ] Encrypt credentials

**Priority:** P0 (Must Have)

---

#### US-14: User Management
**As an** Admin  
**I want to** manage users and permissions  
**So that** I can control access to features

**Acceptance Criteria:**
- [ ] Create/edit/delete users
- [ ] Assign roles (Admin, User, Viewer, Developer)
- [ ] Set permissions per feature
- [ ] View user activity logs

**Priority:** P1 (Should Have)

---

#### US-15: System Settings
**As an** Admin  
**I want to** configure system settings  
**So that** I can optimize performance and behavior

**Acceptance Criteria:**
- [ ] Configure AI model settings
- [ ] Set cache TTL
- [ ] Configure rate limits
- [ ] View system logs

**Priority:** P2 (Nice to Have)

## 5. Non-Functional Requirements

### 5.1 Performance
| Metric | Requirement |
|--------|-------------|
| Schema load time | < 2 seconds |
| Query response time | < 5 seconds |
| Vector conversion | < 10 minutes for 100 tables |
| Concurrent users | 50+ |
| System uptime | 99.9% |

### 5.2 Security
- Authentication: JWT with refresh tokens
- Authorization: Role-based access control
- Encryption: TLS 1.3 for all connections, AES-256 encryption at rest
- Audit: Log all data access
- Password: bcrypt hashing

### 5.3 Scalability
- Horizontal scaling for backend services
- Connection pooling for database
- Caching for frequently accessed data
- Async processing for long-running tasks

### 5.4 Usability
- Responsive design (desktop + tablet)
- Intuitive UI with < 3 clicks to complete tasks
- Comprehensive error messages
- Online help and documentation

### 5.5 Compatibility
- Oracle: 12c, 18c, 19c, 21c
- Browsers: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- OS: Windows 10+, macOS 12+, Ubuntu 20.04+

## 6. Constraints

### Technical Constraints
- Must use Oracle JDBC for database connection
- Must use pgvector for vector storage
- Must use OpenAI API for text-to-SQL
- Must support Vietnamese language

### Business Constraints
- Budget: Self-funded (~$0)
- Timeline: 8 weeks for MVP
- Team: 1 Solo Developer (Multi-role: Backend + Frontend + AI + DBA)

### Regulatory Constraints
- Data privacy: Internal data only (no external compliance required)
- Data retention: 1 year for query history
- Audit requirements: Detailed logging for production

## 7. Assumptions

1. Oracle Database is accessible from application server
2. OpenAI API is available and reliable
3. Users have basic computer literacy
4. Network bandwidth is sufficient for real-time queries
5. Data volume is moderate (1-10GB)

## 8. Dependencies

### External Dependencies
- Oracle Database (12c+)
- PostgreSQL 15+ with pgvector
- OpenAI API access
- Docker runtime

### Internal Dependencies
- Network connectivity to Oracle DB
- SSL certificates for HTTPS
- Domain name and DNS configuration

## 9. Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| User adoption | 80% of target users | Active users / Total users |
| Query accuracy | > 90% | Correct queries / Total queries |
| User satisfaction | > 4/5 | Survey score |
| System uptime | 99.9% | Uptime / Total time |
| Conversion success | > 95% | Successful conversions / Total |

## 10. Out of Scope

### Phase 1 (MVP)
- ❌ Multi-database support (PostgreSQL, MySQL)
- ❌ Real-time data synchronization
- ❌ Advanced ML model training
- ❌ Mobile application
- ❌ Offline mode

### Future Phases
- Phase 2: Multi-database support
- Phase 3: Real-time sync
- Phase 4: Custom model training
- Phase 5: Mobile app

## 11. Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Oracle connection issues | High | Medium | Connection pool, retry logic |
| AI accuracy thấp | High | Medium | Fine-tune prompts, validation |
| Vector conversion chậm | Medium | Low | Batch processing, async |
| Scope creep | Medium | High | Strict change control |
| Team turnover | High | Low | Documentation, knowledge sharing |

### Additional Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| AWS service outage | High | Low | Multi-AZ deployment, backup plan |
| OpenAI API rate limits | High | Medium | Fallback to local LLM (Llama 2) |
| Oracle XE limitations | Medium | Medium | Monitor storage/CPU usage, upgrade plan |

## 12. Approval

**Note:** This section will be completed after stakeholder review and sign-off using REVIEW_CHECKLIST.md

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Project Sponsor | locpn2 | 27/03/2026 | ______________ |
| Technical Lead | locpn2 | 27/03/2026 | ______________ |
| Product Owner | locpn2 | 27/03/2026 | ______________ |
| DBA Representative | locpn2 | 27/03/2026 | ______________ |
| AI Engineer | locpn2 | 27/03/2026 | ______________ |

---

**Document Version**: 1.1  
**Last Updated**: 27/03/2026  
**Next Review**: 03/04/2026
