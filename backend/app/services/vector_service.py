import os
import faiss
import numpy as np
import pickle
from typing import List, Dict
from sentence_transformers import SentenceTransformer


class VectorService:
    """
    Local Vector Store using FAISS.
    Converts textbook chunks into searchable mathematical vectors.
    """

    def __init__(self, subject_name: str):
        self.subject_name = subject_name.replace(" ", "_")
        self.index_path = f"backend/data/indices/{self.subject_name}.index"
        self.metadata_path = f"backend/data/indices/{self.subject_name}.pkl"

        # Ensure the index directory exists
        os.makedirs("backend/data/indices", exist_ok=True)

        # Load the lightest, high-performance local model (runs on CPU)
        # Model: all-MiniLM-L6-v2 (Size: ~80MB)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.metadata = []

    def create_index(self, chunks: List[str], source_files: List[str]):
        """
        Takes text chunks, embeds them, and saves a local FAISS index.
        """
        if not chunks:
            return

        # 1. Convert text chunks to numerical vectors (embeddings)
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        embeddings = np.array(embeddings).astype('float32')

        # 2. Initialize FAISS index (L2 distance for similarity)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

        # 3. Save metadata (the actual text) to link back after search
        self.metadata = [{"content": chunk, "source": src} for chunk, src in zip(chunks, source_files)]

        # 4. Risk-Free Persistence: Save to local disk
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)

    def load_index(self) -> bool:
        """
        Loads the local index from disk if it exists.
        """
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
            return True
        return False

    def search(self, query: str, k: int = 5) -> str:
        """
        Searches the local index for the most relevant textbook context.
        """
        if self.index is None:
            if not self.load_index():
                return "No reference material found for this subject."

        # 1. Embed the user's query
        query_vector = self.model.encode([query]).astype('float32')

        # 2. Search FAISS for top 'k' matches
        distances, indices = self.index.search(query_vector, k)

        # 3. Retrieve and combine the text from metadata
        relevant_chunks = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata):
                relevant_chunks.append(self.metadata[idx]["content"])

        return "\n\n".join(relevant_chunks)