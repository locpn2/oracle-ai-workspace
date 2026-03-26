# OracleVision Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 300 -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
ENV DATABASE_URL=sqlite:///./oraclevision.db
ENV CHROMA_PERSIST_DIR=/app/chroma_db

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
