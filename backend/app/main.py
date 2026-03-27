from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .core.exceptions import add_exception_handlers
from .api.v1 import auth, schema, query, vector

app = FastAPI(
    title="OracleVision API",
    description="AI-Powered Oracle Database Visualization",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://frontend",
        "http://frontend:80",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_exception_handlers(app)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(schema.router, prefix="/api/v1/schema", tags=["schema"])
app.include_router(query.router, prefix="/api/v1/query", tags=["query"])
app.include_router(vector.router, prefix="/api/v1/vector", tags=["vector"])


@app.get("/")
async def root():
    return {"message": "OracleVision API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
