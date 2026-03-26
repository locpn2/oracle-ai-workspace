# Project Brief - VecBase

## Tên dự án
VecBase - Kết hợp Vector và Database

## Mục tiêu
Xây dựng công cụ trực quan hóa dữ liệu Oracle DB với khả năng AI-powered query và chuyển đổi RDBMS sang Vector DB.

## Vấn đề giải quyết
1. **Khó hiểu cấu trúc DB** - Người dùng không chuyên không thể hiểu được Oracle DB có những gì
2. **Query phức tạp** - Cần SQL knowledge để truy vấn dữ liệu
3. **AI integration khó khăn** - Không có cách dễ dàng để tích hợp AI với RDBMS
4. **Vector DB setup phức tạp** - Chuyển đổi từ RDBMS sang Vector DB thủ công và mất thời gian

## Phạm vi dự án

### Tính năng chính
1. **Trực quan hóa dữ liệu Oracle DB**
   - Biểu đồ ERD tự động sinh
   - Schema browsing với UI thân thiện
   - Metadata exploration

2. **AI truy vấn dữ liệu**
   - Text-to-SQL conversion
   - Natural language query
   - Vector-based semantic search

3. **Mô hình hóa dữ liệu theo nhóm**
   - Auto-clustering tables
   - Domain grouping
   - Relationship mapping

4. **Chuyển đổi RDBMS sang Vector DB**
   - Automated conversion pipeline
   - Schema mapping
   - Data embedding generation

### Out of Scope
- Real-time data synchronization
- Multi-database support (chỉ Oracle trong phase 1)
- Advanced ML model training

## Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| DBA | Database Administrator | Schema management, performance |
| Data Analyst | Người phân tích dữ liệu | Easy data access, visualization |
| Developer | Lập trình viên | API integration, automation |
| AI Engineer | Kỹ sư AI | Vector DB, embeddings |

## Success Criteria
- [ ] Non-technical user có thể hiểu DB structure trong < 5 phút
- [ ] AI query accuracy > 85%
- [ ] Vector conversion time < 10 phút cho 100 tables
- [ ] User satisfaction score > 4/5

## Timeline
- Phase 1 (Requirement): Tuần 1
- Phase 2 (Design): Tuần 2
- Phase 3 (Implementation): Tuần 3-6
- Phase 4 (Testing): Tuần 7
- Phase 5 (Deployment): Tuần 8
- Phase 6 (Maintenance): Tuần 9+

## Team
- Backend: 1 developer (Java/Spring Boot)
- Frontend: 1 developer (React)
- AI/ML: 1 engineer
- DevOps: 1 engineer (part-time)