Bạn với vai trò là một chuyên gia domain expert & solution architect, hãy giúp tôi hoàn thiện requirement chi tiết cho dự án "Oracle DB Visualization & RDBMS-to-Vector Converter". Dưới đây là yêu cầu ban đầu, bạn hãy bổ sung thêm chi tiết kỹ thuật, các bước thực hiện, và các checklist cần thiết để đảm bảo dự án được triển khai thành công và lưu vào tệp `docs\spec\requirement.md`.

Dưới đây là chi tiết yêu cầu của tôi:

---

# Khởi tạo Hệ thống: Oracle DB Visualization & RDBMS-to-Vector Converter

Mục tiêu cốt lõi của dự án là xây dựng một công cụ hỗ trợ người dùng trích xuất cấu trúc (Schema) từ Oracle DB để trực quan hóa (dưới dạng biểu đồ), và chuyển đổi các bản ghi dữ liệu (Rows) sang Vector DB (PostgreSQL + pgvector) với sự hỗ trợ của mô hình trí tuệ nhân tạo Google Gemini AI, từ đó cung cấp tính năng truy vấn Text-To-SQL sinh động.

## 1. Mô hình kiến trúc (Architecture Overview)

Hệ thống được thiết kế theo mô hình Microservices hoặc Monolith tùy quy mô, tập trung vào 3 lớp chính

**Sơ đồ luồng dữ liệu (Visual Flow):**

1. Source (Oracle DB) -> Metadata Extractor (Lấy cấu trúc bảng, mối quan hệ).
2. AI Engine (Spring AI + Gemini) -> Natural Language to SQL & Data Embedding.
3. Destination -> Dashboard (Trực quan hóa) & Vector DB (Lưu trữ vector).

**Các thành phần chính:**

- **Backend:** Spring Boot 3.x + Spring AI.
- **Frontend:** React + Tailwind CSS + D3.js (để vẽ sơ đồ quan hệ DB trực quan).
- **Database:** Oracle DB (Nguồn), PostgreSQL + pgvector (để làm Vector DB).
- **AI:** Google Gemini API (Phân tích ngữ nghĩa).

## 2. Danh sách việc cần làm (Todo List)

**Giai đoạn 1:** Khởi tạo & Kết nối

- [ ] Khởi tạo GitHub Repository.
- [ ] Cấu hình docker-compose cho Oracle DB (nếu chưa có), PostgreSQL (Vector Store) và App.
- [ ] Thiết lập dự án Spring Boot với các dependency: spring-ai-bom, spring-boot-starter-data-jpa, ojdbc11.

**Giai đoạn 2:** Trực quan hóa & Truy vấn A

- [ ] Viết Module trích xuất Metadata (Table, Column, Constraints) từ Oracle.
- [ ] Xây dựng API trả về cấu trúc DB dưới dạng JSON cho Frontend vẽ sơ đồ.
- [ ] Tích hợp Spring AI để chuyển đổi câu hỏi tự nhiên (Chat) sang câu lệnh SQL (Text-to-SQL).

**Giai đoạn 3:** RDBMS to Vector DB (Tính năngtrọng tâm)

- [ ] Thiết kế logic "Flattening": Chuyển đổi các dòng dữ liệu quan hệ thành các đoạn văn bản (Documents) có ý nghĩa.
- [ ] Sử dụng Embedding Model của Gemini để vector hóa các Documents này.
- [ ] Lưu trữ Vector vào PostgreSQL (pgvector).

**Giai đoạn 4:** Deployment

- [ ] Viết Dockerfile cho Backend và Frontend.
- [ ] Triển khai CI/CD cơ bản (GitHub Actions).

## 3. Manual Verification

- **Infrastructure:** Chạy docker-compose up -d và đảm bảo PostgreSQL vector store port 5432 đang lắng nghe.
- **Schema Extract API:** Khởi động backend App, gọi cURL tới /api/schema để thu về JSON có liệt kê ít nhất 1 bảng có sẵn trong Oracle.
- **Frontend Dashboard:** Chạy npm dev trên folder React, mở trình duyệt trên port hiển thị UI và theo dõi D3.js vẽ bảng Database.
- **End-to-End Chat:** Nhập câu "Tìm tất cả nhân viên có lương cao hơn Giám đốc" -> Xem log backend generate SQL gì và hiển thị kết quả truy xuất từ DB trả ra màn hình thế nào. Đồng thời thử chức năng Flattening một bảng để đưa vector vào DB postgres thành công.

## 4. Danh sách kiểm tra (Checklist) toàn diện

- [ ] Mã nguồn: Code có unit test cho phần chuyển đổi dữ liệu không?
- [ ] Bảo mật: Thông tin kết nối Oracle có được lưu trong biến môi trường (.env) không?
- [ ] Hiệu suất: Đã xử lý phân trang (Pagination) khi trích xuất dữ liệu lớn từ Oracle chưa?
- [ ] AI: Prompt có chống được SQL Injection (với Text-to-SQL) không?
- [ ] Vector: Đã chọn đúng hàm đo khoảng cách (Cosine Similarity) cho Vector DB chưa?

## 5. Commit & Test Rule

- Mỗi khi hoàn tất một giai đoạn (Phase), bắt buộc phải thực hiện Unit Test để đảm bảo logic cốt lõi hoạt động đúng.
- Sau khi test thành công, thực hiện Commit Git với nội dung mô tả chi tiết các tính năng đã hoàn thành.

---

IMPORTANT:

- DO NOT GENERATE CODE.
- Chỉ cung cấp làm rõ requirement, tạo hướng dẫn, checklist, và các bước thực hiện chi tiết để đảm bảo dự án được triển khai thành công.