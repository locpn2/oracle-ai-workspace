# Active Context - VecBase

## Công việc hiện tại

### Trạng thái: Phase 1 - Requirement Gathering
**Ngày bắt đầu**: 26/03/2026
**Ngày dự kiến hoàn thành**: 02/04/2026

### Đã hoàn thành
- [x] Khám phá AI-SDLC-Workflow
- [x] Phân tích yêu cầu VecBase từ docs/requirement.md
- [x] Đánh giá độ phù hợp của workflow
- [x] Lập kế hoạch thực hiện
- [x] Thiết lập Memory Bank:
  - [x] projectbrief.md
  - [x] productContext.md
  - [x] techContext.md
  - [x] systemPatterns.md
  - [x] activeContext.md (đang tạo)
  - [ ] progress.md

### Đang thực hiện
- [x] Hoàn thiện Memory Bank setup
- [x] Bắt đầu Requirement Gathering theo workflow
- [x] Tạo SPEC.md v1.0 với 15 user stories
- [ ] Requirements Validation (review với stakeholders)

### Sắp tới (Tuần 1)
- [ ] Phase 1.1: Kickoff Meeting
  - Xác định stakeholders chi tiết
  - Document business goals
  - Define success criteria
- [ ] Phase 1.2: User Stories Discovery
  - Tạo user stories cho từng persona
  - Prioritize features
  - Define acceptance criteria
- [ ] Phase 1.3: Scope Definition
  - In-scope features
  - Out-of-scope features
  - Assumptions & dependencies
- [ ] Phase 1.4: Requirements Validation
  - Review với stakeholders
  - Finalize SPEC.md

## Quyết định quan trọng

### Đã quyết định
1. **Tech Stack**: Java 21 + Spring Boot 3.2 + React 18
2. **Architecture**: Hexagonal Architecture (Ports & Adapters)
3. **Vector DB**: PostgreSQL + pgvector
4. **AI Provider**: OpenAI GPT-4
5. **Workflow**: AI-SDLC Workflow với 6 phases

### Cần quyết định
1. **Authentication method**: JWT vs OAuth2 vs SAML?
2. **Deployment target**: AWS vs Azure vs On-premise?
3. **LLM fallback strategy**: Nếu OpenAI down, dùng gì?
4. **Data privacy**: Có cần anonymize data không?

## Patterns & Preferences

### Coding Standards
- **Java**: Google Java Style Guide
- **TypeScript**: Airbnb Style Guide
- **Testing**: TDD approach, 80% coverage target

### Git Workflow
- **Branch strategy**: GitFlow
- **Commit format**: Conventional Commits
- **PR reviews**: Required before merge

### Documentation
- **API**: OpenAPI 3.0 (Swagger)
- **Code**: Javadoc + JSDoc
- **Architecture**: C4 Model diagrams

## Learnings & Insights

### Từ requirement analysis
1. **User diversity**: 4 loại users với needs khác nhau
2. **Complexity**: Oracle DB integration phức tạp hơn expected
3. **AI accuracy**: Text-to-SQL cần fine-tuning cho Oracle syntax

### Từ workflow evaluation
1. **Parallel execution**: Có thể chạy song song Design và Setup
2. **Quality gates**: Rất quan trọng để đảm bảo chất lượng
3. **Documentation**: Cần invest thời gian upfront

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Oracle connection issues | High | Medium | Use connection pool, retry logic |
| AI accuracy thấp | High | Medium | Fine-tune prompts, add validation |
| Vector conversion chậm | Medium | Low | Batch processing, async jobs |
| Scope creep | Medium | High | Strict scope definition, change control |

## Communication

### Stakeholders
- **Project Sponsor**: [TBD]
- **Technical Lead**: [TBD]
- **End Users**: DBA, Data Analyst, AI Engineer, Developer

### Meeting Schedule
- **Daily standup**: 9:00 AM (khi team formed)
- **Weekly review**: Friday 2:00 PM
- **Sprint planning**: Every 2 weeks

## Next Actions

### Hôm nay (26/03/2026)
- [x] Hoàn thiện Memory Bank setup (6 files)
- [x] Tạo progress.md
- [x] Bắt đầu Requirement Gathering
- [x] Tạo SPEC.md v1.0 với 15 user stories đầy đủ acceptance criteria

### Ngày mai (27/03/2026)
- [ ] Draft SPEC.md
- [ ] Create user stories template
- [ ] Define acceptance criteria format

### Tuần này
- [ ] Complete Phase 1: Requirement
- [ ] Prepare for Phase 2: Design