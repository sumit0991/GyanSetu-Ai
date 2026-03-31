import os
from backend.app.services.pdf_processor import PDFProcessor
from backend.app.services.vector_service import VectorService


class RAGEngine:
    def __init__(self, subject: str, path: str = None):
        """
        Initializes the RAG Engine.
        If a path is provided, it checks for an existing index or builds a new one.
        """
        self.subject = subject
        self.upload_path = path  # The folder containing the uploaded PDFs
        self.vector_service = VectorService(subject)

        # Risk-Free Initialization: Ensure we have a searchable index
        self._prepare_engine()

    def _prepare_engine(self):
        """
        Internal logic to either load an existing index or create a new one
        from the uploaded files.
        """
        # 1. Try to load existing index to save time (Risk-free efficiency)
        if self.vector_service.load_index():
            print(f"Index for {self.subject} loaded from disk.")
            return

        # 2. If no index exists and we have files, build it now
        if self.upload_path and os.path.exists(self.upload_path):
            print(f"Building new index for {self.subject}...")

            # Extract text using our PDFProcessor
            raw_data = PDFProcessor.extract_text_from_folder(self.upload_path)

            all_chunks = []
            all_sources = []

            for item in raw_data:
                chunks = PDFProcessor.chunk_text(item["content"])
                all_chunks.extend(chunks)
                all_sources.extend([item["source"]] * len(chunks))

            # Create the index
            if all_chunks:
                self.vector_service.create_index(all_chunks, all_sources)
            else:
                print("Risk Alert: No text could be extracted from the PDFs.")
        else:
            print(f"Waiting for files to index for subject: {self.subject}")

    def get_context(self, query: str):
        """
        Searches the vector store and returns the relevant context and source metadata.
        """
        # Search the local FAISS index
        # We retrieve the top 4 chunks for a broader context
        context_text = self.vector_service.search(query, k=4)

        # Handle citations from metadata
        # Since our VectorService search returns a combined string, we can
        # refine it to return both text and sources if needed.

        # For a professional academic feel, we extract source info
        if self.vector_service.metadata:
            # Get unique sources from the metadata stored during indexing
            unique_sources = list(set([m["source"] for m in self.vector_service.metadata]))
            citation_string = ", ".join(unique_sources)
        else:
            citation_string = "Uploaded Books"

        return {
            "text": context_text,
            "source": citation_string
        }