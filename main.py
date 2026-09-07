import os
import sys
import warnings
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.vectorstores.pgvector import PGVector
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Environment Setup
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not DATABASE_URL or not GOOGLE_API_KEY:
    raise RuntimeError("DATABASE_URL ya GOOGLE_API_KEY .env file me missing hai.")

if DATABASE_URL.startswith("postgresql://"):
    CONNECTION_STRING = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
else:
    CONNECTION_STRING = DATABASE_URL

# 2. Vector Store & LLM Initialization
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = PGVector(
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
    collection_name="credit_risk_regulations",
    use_jsonb=True
)
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2
)

# 3. FastAPI Application Initialization
app = FastAPI(
    title="Tech Innovators - Credit Risk & Regulatory Decisioning API",
    version="1.0.0",
    description="Automated loan decisioning and regulatory RAG assistant backend."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Pydantic Schemas
class ChatRequest(BaseModel):
    query: str = Field(..., example="What is the difference between TTC and PIT rating philosophies?")

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]

class LoanApplicationRequest(BaseModel):
    applicant_id: str = Field(..., example="APP-1092")
    applicant_name: str = Field(..., example="Rohit Sharma")
    annual_income: float = Field(..., example=850000.0)
    monthly_debt_obligations: float = Field(..., example=28000.0)
    credit_score: int = Field(..., ge=300, le=900, example=680)
    requested_loan_amount: float = Field(..., example=1500000.0)
    loan_purpose: str = Field(..., example="Unsecured Personal Loan")
    delinquencies_last_2_years: int = Field(default=0, example=0)

class LoanDecisionResponse(BaseModel):
    applicant_id: str
    decision: str  # APPROVED, REJECTED, MANUAL_REVIEW
    risk_tier: str  # LOW_RISK, MEDIUM_RISK, HIGH_RISK
    calculated_dti_percentage: float
    decision_reasons: List[str]
    regulatory_explanation: str
    cited_policies: List[str]

# 5. Core Helper Functions
def clean_llm_text(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict) and "text" in b:
                parts.append(b["text"])
            elif hasattr(b, "text") and b.text:
                parts.append(b.text)
            elif isinstance(b, str):
                parts.append(b)
        return "".join(parts).strip()
    return str(content).strip()

def run_rag_inference(query: str, system_prompt_template: str):
    docs = retriever.invoke(query)
    if not docs:
        return "No relevant regulatory documentation found.", []

    context_blocks = []
    sources = set()
    for idx, d in enumerate(docs, 1):
        source = d.metadata.get("source", "Policy Doc")
        page = d.metadata.get("page", None)
        label = f"{source} (Page {page + 1})" if page is not None else source
        sources.add(label)
        context_blocks.append(f"[{label}]\n{d.page_content.strip()}")

    full_context = "\n\n".join(context_blocks)
    prompt = system_prompt_template.format(context=full_context, question=query)

    response = llm.invoke(prompt)
    answer = clean_llm_text(response.content)
    return answer, sorted(list(sources))

# 6. API Endpoints
@app.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "Credit Risk Decisioning Platform",
        "database": "Connected to Supabase PostgreSQL (pgvector)",
        "inference_engine": "gemini-3.5-flash"
    }

@app.post("/api/chat", response_model=ChatResponse)
def regulatory_chat(payload: ChatRequest):
    system_prompt = """You are the Senior Credit Risk AI Specialist for the Bank's Risk Engine.
Answer using strictly the regulatory context provided below. Be concise, professional, and highlight regulatory clauses.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:"""
    try:
        answer, sources = run_rag_inference(payload.query, system_prompt)
        return ChatResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.post("/api/evaluate-loan", response_model=LoanDecisionResponse)
def evaluate_loan_application(app_data: LoanApplicationRequest):
    # DTI Calculation: (Annual Debt / Annual Income) * 100
    monthly_income = app_data.annual_income / 12.0
    dti = round((app_data.monthly_debt_obligations / monthly_income) * 100, 2)

    decision_reasons = []
    decision = "APPROVED"
    risk_tier = "LOW_RISK"

    # Automated Rule Engine (Basel / Retail Risk Standards)
    if app_data.delinquencies_last_2_years > 1:
        decision = "REJECTED"
        risk_tier = "HIGH_RISK"
        decision_reasons.append(f"Multiple recent defaults/delinquencies recorded ({app_data.delinquencies_last_2_years} instances).")

    if app_data.credit_score < 620:
        decision = "REJECTED"
        risk_tier = "HIGH_RISK"
        decision_reasons.append(f"Credit Score ({app_data.credit_score}) below the institutional underwriting threshold of 620.")
    elif 620 <= app_data.credit_score < 700:
        if decision != "REJECTED":
            decision = "MANUAL_REVIEW"
            risk_tier = "MEDIUM_RISK"
        decision_reasons.append(f"Credit Score ({app_data.credit_score}) indicates moderate risk profile requiring second-tier risk review.")

    if dti > 50.0:
        decision = "REJECTED"
        risk_tier = "HIGH_RISK"
        decision_reasons.append(f"Debt-to-Income (DTI) ratio of {dti}% exceeds the maximum regulatory tolerance of 50.0%.")
    elif 40.0 < dti <= 50.0:
        if decision != "REJECTED":
            decision = "MANUAL_REVIEW"
            risk_tier = "MEDIUM_RISK"
        decision_reasons.append(f"Elevated DTI of {dti}% requires credit committee justification.")

    if decision == "APPROVED":
        decision_reasons.append("Applicant satisfies credit score, capacity to repay (DTI), and delinquency policy thresholds.")

    # Explainable AI: RAG synthesizes regulatory backing for this specific loan decision
    explanation_query = (
        f"Explain regulatory underwriting policy rationale for a retail loan application with "
        f"Credit Score: {app_data.credit_score}, DTI: {dti}%, Delinquencies: {app_data.delinquencies_last_2_years}. "
        f"Outcome reached: {decision} ({risk_tier})."
    )

    xai_prompt = """You are the Credit Risk Model Auditor.
Provide a concise, formal 2-paragraph regulatory explanation for this credit decision.
Cite Basel prudential risk standards, repayment capacity norms, or internal rating thresholds from the context.

CONTEXT:
{context}

CASE DETAILS:
{question}

EXPLANATION:"""

    try:
        regulatory_explanation, cited_policies = run_rag_inference(explanation_query, xai_prompt)
    except Exception:
        regulatory_explanation = "Underwriting decision generated based on internal scorecards and risk tolerance rules."
        cited_policies = []

    return LoanDecisionResponse(
        applicant_id=app_data.applicant_id,
        decision=decision,
        risk_tier=risk_tier,
        calculated_dti_percentage=dti,
        decision_reasons=decision_reasons,
        regulatory_explanation=regulatory_explanation,
        cited_policies=cited_policies
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)