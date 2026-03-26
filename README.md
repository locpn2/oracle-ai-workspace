# OracleVision - AI-Powered Oracle Database Visualization

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [API Documentation](#api-documentation)
- [Kiến trúc](#kiến-trúc)

## Giới thiệu

**OracleVision** là một công cụ trực quan hóa dữ liệu Oracle Database với khả năng AI-powered:
- Trực quan hóa ERD cho người dùng (kể cả người không chuyên)
- AI truy vấn dữ liệu bằng ngôn ngữ tự nhiên (Text-to-SQL)
- Mô hình hóa dữ liệu theo nhóm/domain
- **Đặc biệt**: Chuyển đổi RDBMS sang Vector DB để tăng cường xử lý AI

## Tính năng

### 1. ERD Visualization (Accessibility-First)
- Biểu đồ ERD tương tác với D3.js
- Hỗ trợ accessibility: screen reader, keyboard navigation, high contrast
- Zoom, pan, và các thao tác drag-drop
- Click để xem chi tiết bảng

### 2. AI Text-to-SQL Query
- Chuyển đổi câu hỏi tiếng Việt/Anh sang Oracle SQL
- Giao diện chat AI để tương tác
- Lịch sử truy vấn
- Hỗ trợ nhiều LLM providers (OpenAI, Anthropic Claude)

### 3. Data Grouping
- Tạo nhóm dữ liệu theo domain (Sales, HR, Finance...)
- Gán bảng vào nhóm
- Màu sắc phân biệt
- Lọc theo nhóm trong ERD

### 4. RDBMS to Vector DB Conversion
- Chuyển đổi dữ liệu Oracle sang vector embeddings
- Tích hợp ChromaDB (local) hoặc pgvector
- Semantic search - tìm kiếm bằng ngôn ngữ tự nhiên
- Incremental sync

## Cài đặt

### Yêu cầu
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (khuyến nghị)
- Oracle Instant Client (optional)

### Cách 1: Docker (Khuyến nghị)

```bash
# Clone repository
git clone <repository-url>
cd oracle-ai-workspace

# Copy và chỉnh sửa environment file
cp .env.example .env
# Edit .env với API keys của bạn

# Build và chạy với Docker Compose
docker-compose up -d
```

Ứng dụng sẽ chạy tại:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Cách 2: Local Development

```bash
# Backend
cd src/backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend (terminal khác)
cd src/frontend
npm install
npm run dev
```

## Sử dụng

### 1. Thêm kết nối Oracle
1. Truy cập trang "Kết nối"
2. Điền thông tin Oracle Database (host, port, service name/sid, username, password)
3. Nhấn "Test" để kiểm tra kết nối
4. Lưu kết nối

### 2. Xem ERD
1. Truy cập trang "ERD"
2. Chọn kết nối và schema
3. Sơ đồ ERD sẽ tự động hiển thị
4. Click vào bảng để xem chi tiết

### 3. AI Query
1. Truy cập trang "AI Truy vấn"
2. Chọn kết nối
3. Nhập câu hỏi bằng tiếng Việt/Anh
4. AI sẽ tạo SQL và bạn có thể thực thi

### 4. Vectorization
1. Truy cập trang "Vector DB"
2. Tạo collection mới từ bảng Oracle
3. Trigger sync để tạo embeddings
4. Sử dụng semantic search

## API Documentation

API documentation có sẵn tại: http://localhost:8000/docs (Swagger UI)

### Endpoints chính:

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | /api/v1/connections | Tạo kết nối mới |
| GET | /api/v1/connections | Danh sách kết nối |
| POST | /api/v1/connections/{id}/test | Test kết nối |
| GET | /api/v1/schemas/{id}/erd | Lấy dữ liệu ERD |
| POST | /api/v1/ai/query | Text-to-SQL |
| POST | /api/v1/vector/sync/{id} | Trigger vectorization |

## Kiến trúc

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React + TypeScript)             │
│  ERD Viewer | AI Chat | Data Groups | Vector Search            │
└─────────────────────────────────────────────────────────────────┘
                              │ REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI + Python)                   │
│  Oracle Client | AI/LLM Router | Embedding Service | Vector DB  │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Oracle DB     │    │ ChromaDB      │    │ LLM APIs     │
│ (Source)      │    │ (Vectors)     │    │ (OpenAI/etc) │
└───────────────┘    └───────────────┘    └───────────────┘
```

## License

MIT License
