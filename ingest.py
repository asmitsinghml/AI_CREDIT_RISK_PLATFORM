import os
import glob
from dotenv import load_dotenv
from tqdm import tqdm

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL .env file me nahi mila!")

if DATABASE_URL.startswith("postgresql://"):
    CONNECTION_STRING = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
else:
    CONNECTION_STRING = DATABASE_URL

COLLECTION_NAME = "credit_risk_regulations"
DOCS_DIR = "./docs"
BATCH_SIZE = 64  # Supabase timeout bachane ke liye micro-batching

print("1. Embedding Model initialize ho raha hai...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""]
)

def run_ingestion():
    pdf_files = glob.glob(os.path.join(DOCS_DIR, "*.pdf"))
    total_files = len(pdf_files)
    print(f"Total PDFs found: {total_files}")

    if total_files == 0:
        print("Error: docs/ folder khali hai! PDFs add karo.")
        return

    # Vector store initialization
    vector_store = PGVector(
        connection_string=CONNECTION_STRING,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
        use_jsonb=True
    )

    print("\nSupabase me upload shuru ho raha hai...\n")
    success_count = 0

    for file_path in tqdm(pdf_files, desc="Processing Files"):
        file_name = os.path.basename(file_path)
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()

            if not pages:
                print(f"\n[Warning] Khali file mili ya read nahi hui: {file_name}")
                continue

            chunks = text_splitter.split_documents(pages)

            for chunk in chunks:
                chunk.metadata["source"] = file_name

            # Safe micro-batching
            for i in range(0, len(chunks), BATCH_SIZE):
                batch = chunks[i:i + BATCH_SIZE]
                vector_store.add_documents(batch)

            success_count += 1

        except Exception as e:
            print(f"\n[Skip] {file_name} me issue aaya: {e}")
            continue

    print(f"\nCompleted! {success_count}/{total_files} files Supabase me permanently save ho gayi hain.")

if __name__ == "__main__":
    run_ingestion()