# Testing Guide

## Running Tests

### Backend Tests
```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_services.py

# Run with coverage
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend

# Run tests (if configured)
npm test

# Build to check for errors
npm run build
```

## Test Structure

```
backend/tests/
├── conftest.py          # Pytest fixtures
├── test_services.py     # Service tests
└── README.md           # This file
```

## Test Categories

### Unit Tests
- Text-to-SQL service logic
- Security functions (password hashing, token generation)
- Mock data validation
- SQL table extraction

### Integration Tests
- API endpoint testing (manual)
- Database connection testing (requires Docker)

## Test Coverage

Current test coverage targets:
- Unit tests: 80%
- Integration tests: 60%

## Running with Docker

To run tests with full infrastructure:
```bash
docker-compose up -d

# Run tests
docker-compose exec backend pytest
```

## Manual Testing Checklist

### Authentication
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Register new user
- [ ] Token refresh
- [ ] Logout

### ERD Viewer
- [ ] Load ERD with mock data
- [ ] Zoom/pan functionality
- [ ] Export to PNG
- [ ] Export to SVG

### Query Execution
- [ ] Text-to-SQL conversion
- [ ] SQL execution with results
- [ ] Query history
- [ ] Export to CSV
- [ ] Export to JSON
- [ ] Execution plan view

### Schema Management
- [ ] View tables list
- [ ] View table details
- [ ] Create schema group
- [ ] Vector sync functionality
- [ ] Semantic search

### Vector Database
- [ ] Sync schema to vector DB
- [ ] Semantic search for tables
- [ ] View sync status