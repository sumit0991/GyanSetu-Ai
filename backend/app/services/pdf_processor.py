import fitz  # PyMuPDF
import os
import re
from typing import List, Dict


class PDFProcessor:
    """
    Industry-standard PDF text extraction service.
    Handles local file reading, cleaning, and chunking for the RAG engine.
    """

    @staticmethod
    def extract_text_from_folder(folder_path: str) -> List[Dict[str, str]]:
        """
        Reads all PDFs in a subject folder and extracts text with metadata.
        Returns a list of dictionaries containing text and the source filename.
        """
        extracted_data = []

        if not os.path.exists(folder_path):
            print(f"Risk Alert: Folder {folder_path} does not exist.")
            return extracted_data

        # Filter for PDF files only
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]

        for filename in pdf_files:
            file_path = os.path.join(folder_path, filename)
            try:
                # Open the document
                doc = fitz.open(file_path)
                full_text = ""

                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    # Use 'block' method to maintain reading order in textbooks
                    text = page.get_text("blocks")
                    for block in text:
                        # block[4] contains the actual text string
                        full_text += block[4] + " "

                # Clean the text (remove multiple spaces and non-standard characters)
                cleaned_text = PDFProcessor._clean_text(full_text)

                extracted_data.append({
                    "content": cleaned_text,
                    "source": filename
                })
                doc.close()

            except Exception as e:
                print(f"Error processing {filename}: {e}")

        return extracted_data

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Internal utility to sanitize text for better LLM processing.
        """
        # Remove repeated newlines and extra spaces
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        # Remove basic illegal characters that might break JSON responses
        text = text.encode("ascii", "ignore").decode()
        return text.strip()

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Splits text into overlapping chunks.
        Crucial for RAG to ensure context isn't lost at the edges of a paragraph.
        """
        chunks = []
        words = text.split()

        # A simple but effective sliding window approach
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            if i + chunk_size >= len(words):
                break

        return chunks