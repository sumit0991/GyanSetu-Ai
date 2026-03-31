import fitz  # PyMuPDF
import re


class PDFProcessor:
    @staticmethod
    def extract_text_with_metadata(pdf_path):
        doc = fitz.open(pdf_path)
        pages_content = []
        current_unit = "General"

        for page_num, page in enumerate(doc):
            text = page.get_text("text")

            # Heuristic: Find Unit/Chapter headers
            lines = text.split('\n')
            for line in lines[:5]:  # Usually headers are at the top
                if re.match(r'^(Unit|Chapter|Module|Part)\s+\d+', line, re.IGNORECASE):
                    current_unit = line.strip()
                    break

            pages_content.append({
                "text": text,
                "metadata": {
                    "page": page_num + 1,
                    "unit": current_unit
                }
            })
        return pages_content

    @staticmethod
    def split_into_chunks(pages_content, chunk_size=700, overlap=100):
        chunks = []
        metadatas = []

        for item in pages_content:
            text = item['text']
            words = text.split()
            for i in range(0, len(words), chunk_size - overlap):
                chunk_text = " ".join(words[i:i + chunk_size])
                chunks.append(chunk_text)
                metadatas.append(item['metadata'])

        return chunks, metadatas