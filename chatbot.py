import os
import sys
import warnings

# Terminal ko clean rakhne ke liye deprecation aur internal warnings suppress karna
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Environment variables validation
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not DATABASE_URL:
  print("\n[Error] DATABASE_URL .env file me nahi mila.")
  sys.exit(1)

if not GOOGLE_API_KEY:
  print("\n[Error] GOOGLE_API_KEY .env file me nahi mila.")
  sys.exit(1)

# SQLAlchemy driver prefix formatting
if DATABASE_URL.startswith("postgresql://"):
  CONNECTION_STRING = DATABASE_URL.replace(
      "postgresql://", "postgresql+psycopg2://", 1
  )
else:
  CONNECTION_STRING = DATABASE_URL

COLLECTION_NAME = "credit_risk_regulations"

# 2. Embedding Model (Identical to Ingestion)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 3. Supabase PGVector Store Connection
vector_store = PGVector(
    connection_string=CONNECTION_STRING,
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
    use_jsonb=True,
)

# Top 4 most relevant chunks
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

# 4. Verified Production Model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
)

# 5. Production Banking Regulatory Prompt
SYSTEM_PROMPT = """You are the Senior Credit Risk AI Specialist for the Bank's Risk & Decisioning Engine.
Answer the question using ONLY the provided regulatory documents, credit risk methodologies, and policy context.

Operational Directives:
1. Grounding: Rely strictly on the formulas, regulatory rules (Basel II/III/IV, IFRS 9), and credit metrics (PD, LGD, EAD, ECL) in the context.
2. Zero Hallucination: If the context is insufficient to answer the question, state:
   "The provided banking policy and model documentation does not contain sufficient information to answer this query."
3. Format: Return a clean, executive-ready explanation using structured Markdown with bold headers and crisp bullet points.

--------------------
CONTEXT:
{context}
--------------------

QUESTION:
{question}

DETAILED REGULATORY ANSWER:"""


def clean_response_text(content) -> str:
  """Extracts clean human-readable text from LangChain response objects,

  stripping out API metadata, raw dictionary wrappers, and signatures.
  """
  if isinstance(content, str):
    return content.strip()

  if isinstance(content, list):
    text_segments = []
    for item in content:
      if isinstance(item, dict):
        if "text" in item and item["text"]:
          text_segments.append(item["text"])
      elif hasattr(item, "text") and item.text:
        text_segments.append(item.text)
      elif isinstance(item, str):
        text_segments.append(item)
    return "".join(text_segments).strip()

  return str(content).strip()


def ask_assistant(query: str):
  """Queries Supabase PGVector, compiles regulatory context,

  and returns clean parsed answers with exact document citations.
  """
  try:
    retrieved_docs = retriever.invoke(query)
  except Exception as e:
    return f"Vector Store Retrieval Error: {e}", []

  if not retrieved_docs:
    return (
        "No matching regulatory or policy documentation found in the database.",
        [],
    )

  # Context compilation & source tracking
  context_blocks = []
  cited_sources = set()

  for idx, doc in enumerate(retrieved_docs, start=1):
    source = doc.metadata.get("source", "Unknown Document")
    page = doc.metadata.get("page", None)
    source_label = f"{source} (Page {page + 1})" if page is not None else source
    cited_sources.add(source_label)

    context_blocks.append(
        f"[Document {idx} | Source: {source_label}]\n{doc.page_content.strip()}"
    )

  context_text = "\n\n".join(context_blocks)
  formatted_prompt = SYSTEM_PROMPT.format(
      context=context_text, question=query
  )

  # LLM invocation
  try:
    raw_response = llm.invoke(formatted_prompt)
    answer = clean_response_text(raw_response.content)
  except Exception as e:
    answer = f"Inference Error: {e}"

  return answer, sorted(list(cited_sources))


# 6. Terminal Interface
if __name__ == "__main__":
  print("\n" + "=" * 72)
  print(" TECH INNOVATORS - CREDIT RISK REGULATORY DECISIONING ENGINE ")
  print(" Vector Store: Supabase PGVector (86 Banking Regulations Live) ")
  print(" LLM Backend: gemini-3.5-flash (Low-latency Inference) ")
  print("=" * 72)
  print("Commands: Enter your query, or type 'exit'/'quit' to leave.\n")

  while True:
    try:
      user_input = input("\nEnter Regulatory / Policy Question: ").strip()

      if user_input.lower() in ["exit", "quit", "q"]:
        print("\nTerminating session. Goodbye!")
        break

      if not user_input:
        continue

      print("\n[Processing] Querying vector space & drafting verified response...")
      final_answer, sources = ask_assistant(user_input)

      print("\n" + "=" * 72)
      print("DECISIONING ENGINE RESPONSE:")
      print("=" * 72)
      print(final_answer)

      print("\n" + "-" * 72)
      print("VERIFIED REGULATORY SOURCES:")
      print("-" * 72)
      if sources:
        for s in sources:
          print(f" • {s}")
      else:
        print(" None")
      print("=" * 72)

    except KeyboardInterrupt:
      print("\nSession interrupted by user. Exiting...")
      break