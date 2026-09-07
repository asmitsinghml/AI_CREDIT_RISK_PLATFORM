from typing import List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from .engine import run_rag_inference

router = APIRouter(tags=["Credit Risk RAG & Decisioning"])

# ==============================================================================
# Request & Response Schemas (Pydantic Models)
# ==============================================================================

class ChatRequest(BaseModel):
    query: str = Field(
        ..., 
        example="What is the difference between Through-The-Cycle (TTC) and Point-In-Time (PIT) rating philosophies?"
    )


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
    decision: str  # APPROVED | REJECTED | MANUAL_REVIEW
    risk_tier: str  # LOW_RISK | MEDIUM_RISK | HIGH_RISK
    calculated_dti_percentage: float
    decision_reasons: List[str]
    regulatory_explanation: str
    cited_policies: List[str]


# ==============================================================================
# Endpoint 1: Regulatory RAG Chat Assistant
# ==============================================================================

@router.post(
    "/api/chat",
    response_model=ChatResponse,
    summary="Regulatory & Credit Risk Policy Q&A Assistant"
)
def regulatory_chat(payload: ChatRequest):
    """Answers banking and policy inquiries using only retrieved Supabase

    PGVector context from 86 ingested regulatory documents.
    """
    system_prompt = """You are the Senior Credit Risk AI Specialist for the Bank's Risk & Decisioning Engine.
Answer the question using ONLY the provided regulatory documents, credit risk methodologies, and policy context.

Directives:
1. Rely strictly on regulatory standards (Basel II/III/IV, IFRS 9) and credit metrics (PD, LGD, EAD, ECL).
2. If the context is insufficient, explicitly state that the documentation does not contain this information.
3. Provide crisp, structured Markdown formatting with bullet points and bold highlights.

--------------------
CONTEXT:
{context}
--------------------

QUESTION:
{question}

DETAILED REGULATORY ANSWER:"""

    try:
        answer, sources = run_rag_inference(payload.query, system_prompt)
        return ChatResponse(answer=answer, sources=sources)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error in RAG engine: {str(exc)}"
        )


# ==============================================================================
# Endpoint 2: Automated Loan Decisioning with Explainable AI (XAI)
# ==============================================================================

@router.post(
    "/api/evaluate-loan",
    response_model=LoanDecisionResponse,
    summary="Automated Loan Underwriting & Regulatory Policy Grounding"
)
def evaluate_loan_application(app_data: LoanApplicationRequest):
    """Evaluates loan applicant eligibility against prudential risk thresholds

    (Credit Score, DTI, Delinquencies) and synthesizes policy backing via RAG.
    """
    # 1. Capacity to Repay Calculation (Debt-To-Income Ratio)
    monthly_income = app_data.annual_income / 12.0
    if monthly_income <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Annual income must be greater than zero."
        )

    dti = round((app_data.monthly_debt_obligations / monthly_income) * 100, 2)

    decision_reasons: List[str] = []
    decision = "APPROVED"
    risk_tier = "LOW_RISK"

    # 2. Institutional Underwriting Policy Engine
    # Rule A: Recent Delinquency Threshold
    if app_data.delinquencies_last_2_years > 1:
        decision = "REJECTED"
        risk_tier = "HIGH_RISK"
        decision_reasons.append(
            f"Multiple recent delinquencies recorded ({app_data.delinquencies_last_2_years} instances in 24 months)."
        )

    # Rule B: Credit Score Underwriting Thresholds
    if app_data.credit_score < 620:
        decision = "REJECTED"
        risk_tier = "HIGH_RISK"
        decision_reasons.append(
            f"Credit score ({app_data.credit_score}) is below the mandatory retail underwriting floor of 620."
        )
    elif 620 <= app_data.credit_score < 700:
        if decision != "REJECTED":
            decision = "MANUAL_REVIEW"
            risk_tier = "MEDIUM_RISK"
        decision_reasons.append(
            f"Credit score ({app_data.credit_score}) indicates moderate probability of default; secondary underwriting review required."
        )

    # Rule C: DTI Policy Caps
    if dti > 50.0:
        decision = "REJECTED"
        risk_tier = "HIGH_RISK"
        decision_reasons.append(
            f"Debt-to-Income (DTI) ratio of {dti}% exceeds the institutional ceiling of 50.0%."
        )
    elif 40.0 < dti <= 50.0:
        if decision != "REJECTED":
            decision = "MANUAL_REVIEW"
            risk_tier = "MEDIUM_RISK"
        decision_reasons.append(
            f"Elevated DTI of {dti}% exceeds the preferred 40.0% benchmark; manual debt verification required."
        )

    if decision == "APPROVED":
        decision_reasons.append(
            "Applicant satisfies all prime underwriting criteria: credit score, DTI ratio, and clear delinquency history."
        )

    # 3. Explainable AI (XAI): Synthesize regulatory justification via RAG
    explanation_query = (
        f"Explain regulatory underwriting policy rationale for a retail loan application with "
        f"Credit Score: {app_data.credit_score}, DTI: {dti}%, Delinquencies: {app_data.delinquencies_last_2_years}. "
        f"Outcome reached: {decision} ({risk_tier})."
    )

    xai_prompt = """You are the Bank Credit Risk Model Auditor and Compliance Officer.
Provide a concise, formal 2-paragraph regulatory explanation for this credit decision.
Cite Basel prudential risk standards, repayment capacity norms, or internal rating thresholds from the context.

CONTEXT:
{context}

CASE DETAILS:
{question}

REGULATORY EXPLANATION:"""

    try:
        regulatory_explanation, cited_policies = run_rag_inference(explanation_query, xai_prompt)
    except Exception:
        regulatory_explanation = (
            "Underwriting decision generated based on internal credit scorecards, "
            "debt service thresholds, and prudential risk management rules."
        )
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