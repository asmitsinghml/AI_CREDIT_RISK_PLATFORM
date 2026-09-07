import os
import warnings
from typing import List, Tuple
from dotenv import load_dotenv

# Suppress internal library deprecation and AFC warnings
warnings.filterwarnings("ignore")

from langchain_community.vectorstores.pgvector import PGVector
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Load and validate environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not DATABASE_URL or not GOOGLE_API_KEY:
    raise RuntimeError("DATABASE_URL ya GOOGLE_API_KEY .env file me missing hai.")

# Ensure SQLAlchemy psycopg2 compatibility
if DATABASE_URL.startswith("postgresql://"):
    CONNECTION_STRING = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
else:
    CONNECTION_STRING = DATABASE_URL

COLLECTION_NAME = "credit_risk_regulations"

# 2. Embedding Model (HuggingFace 384-dim)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 3. Connect to Supabase PGVector
vector_store = PGVector(
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
    use_jsonb=True,
)

# Top 4 most relevant chunks
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

# 4. Verified Inference Model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)


def clean_llm_text(content) -> str:
    """Strips raw dictionary wrappers, LangChain signature metadata,

    and extracts pure Markdown text.
    """
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
            elif hasattr(item, "text") and item.text:
                parts.append(item.text)
            elif isinstance(item, str):
                parts.append(item)
        return "".join(parts).strip()
    return str(content).strip()


def run_rag_inference(query: str, system_prompt_template: str) -> Tuple[str, List[str]]:
    """Retrieves context from Supabase, formats the prompt,

    and returns clean text with audit-ready source citations.
    """
    try:
        docs = retriever.invoke(query)
    except Exception as e:
        return f"Retrieval error from Supabase: {str(e)}", []

    if not docs:
        return "No matching regulatory or policy documentation found in the database.", []

    context_blocks = []
    sources = set()

    for idx, d in enumerate(docs, start=1):
        source = d.metadata.get("source", "Policy Document")
        page = d.metadata.get("page", None)
        source_label = f"{source} (Page {page + 1})" if page is not None else source
        sources.add(source_label)
        context_blocks.append(f"[Document {idx} | Source: {source_label}]\n{d.page_content.strip()}")

    full_context = "\n\n".join(context_blocks)
    formatted_prompt = system_prompt_template.format(context=full_context, question=query)

    try:
        response = llm.invoke(formatted_prompt)
        answer = clean_llm_text(response.content)
    except Exception as e:
        answer = f"LLM inference error: {str(e)}"

    return answer, sorted(list(sources))