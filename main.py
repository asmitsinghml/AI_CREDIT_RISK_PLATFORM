import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import RAG Router directly from your modular package
from rag import rag_router

# 1. Initialize FastAPI Application
app = FastAPI(
    title="AI-Powered Credit Risk Platform API",
    version="1.0.0",
    description="Enterprise Credit Risk Decisioning, Basel Analytics, and Regulatory RAG Assistant.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 2. Configure Cross-Origin Resource Sharing (CORS) for Frontend Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production me frontend domain ke hisab se restrict kar sakte hain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Root & System Health Check Endpoints
@app.get("/", tags=["System"])
def root():
    return {
        "project": "AI-Powered Credit Risk Platform",
        "version": "1.0.0",
        "status": "active",
        "docs_url": "/docs"
    }

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "AI Credit Risk Platform API Gateway",
        "rag_engine": "online (Supabase PGVector + Gemini 3.5 Flash)"
    }

# 4. Mount Modular RAG & Decisioning Endpoints (/api/chat, /api/evaluate-loan)
app.include_router(rag_router)

# 5. Local Execution Entrypoint
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)