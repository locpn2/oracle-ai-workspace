# OracleVision - AI-Powered Oracle Database Visualization

A modern tool for visualizing Oracle databases and querying them using natural language with AI assistance.

## Features

- **ERD Visualization**: Interactive Entity Relationship Diagrams
- **Text-to-SQL**: Convert natural language queries to Oracle SQL
- **Schema Grouping**: Organize tables into logical groups
- **RDBMS → Vector DB**: Sync schema to pgvector for semantic search

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18 + TypeScript + Tailwind CSS |
| Backend | FastAPI + Python 3.11 |
| Database | Oracle XE 21 + PostgreSQL (pgvector) |
| Cache | Redis |
| AI | LangChain (OpenAI, Claude, Ollama) |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd oracle-ai-workspace-opencode

# Start all services
docker-compose up -d

# Access the application
open http://localhost:3000
```

### Local Development

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Demo Credentials

- Email: `demo@oraclevision.com`
- Password: `demo123`

## Project Structure

```
oracle-vision/
├── frontend/           # React SPA
│   ├── src/
│   │   ├── components/ # UI Components
│   │   ├── pages/      # Route Pages
│   │   ├── services/   # API Clients
│   │   ├── stores/     # State Management
│   │   └── types/      # TypeScript Types
│   └── ...
├── backend/            # FastAPI Backend
│   ├── app/
│   │   ├── api/        # API Routes
│   │   ├── core/       # Config & Security
│   │   ├── models/     # Pydantic Models
│   │   ├── services/    # Business Logic
│   │   └── db/         # Database Connections
│   └── ...
├── docker-compose.yml
├── init.sql           # PostgreSQL initialization
├── SPEC.md            # Full specification
└── README.md
```

## Environment Variables

Create `.env` files in respective directories:

**Backend (.env):**
```env
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XEPDB1
ORACLE_USER=system
ORACLE_PASSWORD=your_password

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=oracle_vision
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login` | POST | Login |
| `/api/v1/schema/tables` | GET | List tables |
| `/api/v1/schema/erd` | GET | Get ERD data |
| `/api/v1/query/text-to-sql` | POST | NL to SQL |
| `/api/v1/query/execute` | POST | Execute SQL |
| `/api/v1/vector/sync` | POST | Sync to vector DB |

## License

MIT
