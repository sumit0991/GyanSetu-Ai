import os
import sys
import fitz  # PyMuPDF

# --- PATH FIX ---
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from backend.app.core.config import settings


def index_all_pdfs_in_subject(subject: str):
    print(f"--- Starting Multi-PDF Indexing for: {subject} ---")

    subject_path = os.path.join(settings.RAW_PDF_DIR, subject)
    if not os.path.exists(subject_path):
        print(f"Error: Folder not found at {subject_path}")
        return

    all_text_chunks = []

    # 1. Loop through every PDF in the folder
    pdf_files = [f for f in os.listdir(subject_path) if f.endswith('.pdf')]
    print(f"Found {len(pdf_files)} books: {pdf_files}")

    for filename in pdf_files:
        print(f"Reading {filename}...")
        pdf_path = os.path.join(subject_path, filename)
        doc = fitz.open(pdf_path)

        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            # Split into chunks and add source metadata
            chunks = [p.strip() for p in text.split('\n\n') if len(p) > 100]
            all_text_chunks.extend(chunks)
        doc.close()

    if not all_text_chunks:
        print("Error: No text found in any PDFs.")
        return

    # 2. Create one combined Vector Store
    print(f"Generating embeddings for {len(all_text_chunks)} total chunks...")
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBED_MODEL)

    vector_db = FAISS.from_texts(all_text_chunks, embeddings)

    # 3. Save the single merged index
    save_path = os.path.join(settings.VECTOR_DB_DIR, f"{subject}_faiss")
    vector_db.save_local(save_path)
    print(f"--- Successfully merged {len(pdf_files)} books into {save_path} ---")


if __name__ == "__main__":
    # This will now process EVERYTHING inside 'backend/data/raw_pdfs/DBMS/'
    index_all_pdfs_in_subject("DBMS")