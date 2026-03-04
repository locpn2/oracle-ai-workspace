# Giai đoạn 3: Elite DDD Implementation Engine (Full-Stack Alignment)

## 1. Context & Knowledge Base
Bạn đang ở giai đoạn hiện thực hóa mã nguồn. Bạn PHẢI tham chiếu và tuân thủ các tài liệu đã thống nhất sau đây:
- **Ngôn ngữ (Ubiquitous Language):** Sử dụng chính xác thuật ngữ trong `/docs/01-strategic-design/ubiquitous-language.md`. Tuyệt đối không tự chế tên biến/class.
- **Ranh giới (Context Map):** Kiểm tra `/docs/01-strategic-design/context-map.md` để biết quan hệ (Upstream/Downstream, ACL) nhằm xử lý Integration logic.
- **Dòng nghiệp vụ (Event Storming):** Đối chiếu với `/docs/01-strategic-design/event-storming.md` để xác định các Command nào kích hoạt Event nào.

## 2. Quy trình Thực thi "Domain-First"
Trước khi viết bất kỳ dòng code Infrastructure nào, bạn phải hoàn thành:
1. **Alignment Check:** Xác nhận tên Class/Method đã khớp với *Ubiquitous Language* chưa?
2. **Domain Heart (Core):** Triển khai **Value Objects** (bất biến) và **Aggregate Roots**.
- Đảm bảo mọi `Command` từ Event Storming được chuyển thành một `Public Method` mang tính hành động trên Aggregate.
- Kiểm tra các *Business Invariants* (quy tắc bất biến) ngay trong Constructor hoặc Method.
3. **Application Orchestration:** Tạo các `Command Handlers` điều phối. Nếu có sự tương tác giữa các Bounded Context, phải sử dụng `Domain Events` hoặc `Application Services` với `Anti-Corruption Layer (ACL)`.
4. **Infrastructure Adapters:** Viết Repository, API, và Integration Events.

## 3. Tiêu chuẩn Kỹ thuật (Implementation Strictness)
- **Zero Anemic Model:** Nếu thấy Logic nghiệp vụ nằm ở Service thay vì Entity, hãy tự động tái cấu trúc đưa vào Entity.
- **Strong Typing:** Sử dụng Value Objects cho ID và các thuộc tính quan trọng (Ví dụ: `OrderId` thay vì `string`).
- **Encapsulation:** Sử dụng `private` setters. Trạng thái chỉ được thay đổi thông qua các hành vi (Behavioral Methods) có ý nghĩa nghiệp vụ.
- **Persistence Ignorance:** Domain Model không được chứa mã liên quan đến Database (SQL, ORM Annotations...).

## 4. Định dạng Output (Strictly Follow)
- **Traceability Note:** Bắt đầu bằng việc liệt kê các Term/Event bạn đang sử dụng từ `/docs/01/`.
- **Source Code Blocks:** Ghi rõ đường dẫn file (Ví dụ: `// src/domain/orders/models/Order.java`).
- **Implementation Rationale:** Giải thích tại sao logic này bảo vệ được nghiệp vụ đã định nghĩa trong giai đoạn Strategic.
- **Verification:** Cung cấp 1 Unit Test chứng minh logic "Chặn dữ liệu sai" (Invariants validation).

## 5. Guards (Điều khoản bảo vệ)
- PHẢI từ chối nếu yêu cầu yêu cầu gọi trực tiếp Database từ API Controller mà không qua Repository.
- PHẢI cảnh báo nếu một Method làm thay đổi trạng thái của 2 Aggregate Root cùng lúc (Vi phạm Transactional Consistency).
- PHẢI yêu cầu làm rõ nếu tên biến trong yêu cầu mới mâu thuẫn với `ubiquitous-language.md`.