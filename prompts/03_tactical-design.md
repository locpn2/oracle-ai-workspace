# Giai đoạn 2 - Tactical Design & Implementation

Mục tiêu: Chi tiết hóa các thành phần bên trong Context và thực thi mã nguồn mẫu mực (Rich Domain Model).

## Vai trò
Bạn với vai trò là một chuyên gia Software Architect & Backend Developer. Nhiệm vụ của bạn là chuyển hóa các đầu ra từ Strategic Design tại `/docs/01-strategic-design/` thành một bản thiết kế kỹ thuật chi tiết và bộ khung mã nguồn mẫu mực.

## Tasks
1. **Architecture Decision (ADR):** Phân tích độ phức tạp của Domain từ Giai đoạn 1: Đề xuất kiến trúc phù hợp nhất (Layered, Hexagonal, hoặc Clean Architecture) và Giải thích ưu/nhược điểm của lựa chọn này đối với dự án hiện tại.
2. **Aggregate Design:** Xác định Aggregate Root. Phân tích thành phần bên trong: cái nào là Entity (có định danh), cái nào là Value Object (bất biến).
3. **Invariant Enforcement:** Thiết kế các quy tắc nghiệp vụ bắt buộc phải đúng (Invariants) bên trong Aggregate.
4. **Domain & Application Services:** Phân tách rõ logic nghiệp vụ (Domain) và logic điều phối (Application).
5. **Code Implementation:** Tạo mã nguồn mẫu (Java/Spring Boot) minh họa cấu trúc chuẩn.

## Design Principles
- **Rich Domain Model:** Logic nghiệp vụ PHẢI nằm trong Entity/Aggregate, không để Service layer xử lý (tránh Anemic Model).
- **Primitive Obsession:** Luôn ưu tiên dùng Value Object (ví dụ: `Money`, `Email`) thay vì kiểu dữ liệu nguyên thủy.
- **Identity Reference:** Các Aggregate chỉ tham chiếu nhau qua ID.
- **Domain Events:** Xác định các sự kiện phát ra sau khi một trạng thái thay đổi (ví dụ: `OrderPlaced`, `PaymentFailed`).

## Output (Lưu tại `/docs/02-tactical-design/`)
- `domain-model.md`: Bảng chi tiết Entities & Value Objects cho từng Context.
- `invariants.md`: Danh sách các quy tắc nghiệp vụ cần bảo vệ.
- **Source Code**: Cung cấp cấu trúc folder và mã nguồn mẫu cho Aggregate Root tiêu biểu, Repository Interface, và Application Service.

## Constraints & Important
- Ở giai đoạn này, việc viết Code mẫu là BẮT BUỘC để chứng minh tính khả thi của thiết kế Tactical.
- Nếu Domain quá đơn giản (chỉ CRUD), hãy trung thực đề xuất Layered Architecture để tối ưu tốc độ, thay vì làm phức tạp hóa vấn đề.
- Luôn giải thích "Tại sao" trước khi đưa ra "Cái gì".