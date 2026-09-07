import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL.startswith("postgresql://"):
  CONNECTION_STRING = DATABASE_URL.replace(
      "postgresql://", "postgresql+psycopg2://", 1
  )
else:
  CONNECTION_STRING = DATABASE_URL

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=150
)

file_path = os.path.join("./docs", "Credit Risk Modelling compilation.pdf")

if os.path.exists(file_path):
  loader = PyPDFLoader(file_path)
  pages = loader.load()

  # Stringification: har page aur character ko force string banana
  forced_docs = []
  for p in pages:
    raw_str = str(p.page_content) if p.page_content else ""
    clean_str = raw_str.replace("\x00", "").encode("ascii", "ignore").decode()
    if len(clean_str.strip()) > 30:
      forced_docs.append(clean_str)

  chunks = text_splitter.split_text("\n\n".join(forced_docs))

  final_docs = [
      Document(
          page_content=str(c),
          metadata={"source": "Credit Risk Modelling compilation.pdf"},
      )
      for c in chunks
      if isinstance(c, str) and len(c.strip()) > 10
  ]

  vector_store = PGVector(
      connection_string=CONNECTION_STRING,
      embedding_function=embeddings,
      collection_name="credit_risk_regulations",
      use_jsonb=True,
  )

  for i in range(0, len(final_docs), 64):
    vector_store.add_documents(final_docs[i : i + 64])

  print(f"Compilation PDF uploaded successfully ({len(final_docs)} chunks)!")