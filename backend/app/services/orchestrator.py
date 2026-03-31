import os
from backend.app.services.rag_engine import RAGEngine
from backend.app.services.llm_service import LLMService
from backend.app.services.video_service import VideoService


class CourseOrchestrator:
    def __init__(self, subject: str):
        self.subject = subject
        subject_folder_name = subject.replace(" ", "_")
        upload_path = os.path.join("backend", "data", "uploads", subject_folder_name)
        self.rag = RAGEngine(subject=subject, path=upload_path)
        self.llm = LLMService()

    def generate(self, topic: str):
        # 1. Fetch context from RAG
        rag_response = self.rag.get_context(topic)

        if isinstance(rag_response, dict):
            context = rag_response.get("text", "")
            source_info = rag_response.get("source", "Internal Library")
        else:
            context = rag_response
            source_info = f"{self.subject} Reference Materials"

        # 2. EXHAUSTIVE EXAM-READY PROMPT (Now optimized for Gemini's speed)
        structured_instruction = f"""
        TOPIC: {topic}
        SUBJECT: {self.subject}

        PART 1: STUDY NOTES
        1. <b>DEFINITION:</b><br>(Provide a formal academic definition in 3-4 sentences.)

        2. <b>DETAILED TECHNICAL EXPLANATION:</b><br>(Provide 10-15 sentences of deep technical explanation. 
           Focus on the internal architecture, logic, and working mechanism of {topic}.)

        3. <b>CORE COMPONENTS / LAYERS / PRINCIPLES:</b><br>
           (Crucial: If this topic has sub-components like the 7 OSI Layers, SOLID principles, or specific 
           objectives, you MUST list each one and provide a 2-sentence explanation for EVERY single sub-item. 
           Do not skip any.)

        4. <b>ADVANTAGES & DISADVANTAGES:</b><br>(Provide a comprehensive bulleted list of pros and cons.)

        5. <b>REAL-WORLD EXAMPLE:</b><br>(Describe a practical application or use-case in detail.)

        6. <b>CONCLUSION:</b><br>(Provide a summary conclusion of exactly 10 sentences, discussing 
           the technical significance and future impact of {topic}.)

        7. <b>IMPORTANT EXAM TIPS:</b><br>(Highlight 3-5 critical points students must memorize for finals.)

        <br><i>Source: {source_info}</i>

        PART 2: FLASHCARDS
        Provide 5 active recall questions for exam preparation.
        [Q]: Question?
        [A]: Answer.

        RULES:
        - Use <b> for headers and <br> for spacing.
        - Ensure every "Layer" or "Principle" has its own description.
        - Use provided context first; use your expert internal knowledge to fill any gaps.
        """

        # 3. Generate content using Gemini (Via LLMService)
        raw_result = self.llm.generate_exam_notes(structured_instruction, context)

        # 4. Reliable Parsing for UI
        notes_part = raw_result
        flashcards_data = []

        if "PART 2: FLASHCARDS" in raw_result:
            parts = raw_result.split("PART 2: FLASHCARDS")
            notes_part = parts[0]
            if len(parts) > 1:
                card_section = parts[1]
                cards = card_section.split("[Q]:")
                for c in cards[1:]:
                    if "[A]:" in c:
                        q_a = c.split("[A]:")
                        flashcards_data.append({
                            "question": q_a[0].strip(),
                            "answer": q_a[1].strip()
                        })

        # 5. Fetch curated video logic
        video_data = VideoService.get_curated_video(topic, self.subject)

        # 6. Returning the expanded package
        # MODIFIED: Now returning 'context' so the UI can verify the RAG source
        return {
            "answer": notes_part,
            "video": video_data,
            "flashcards": flashcards_data,
            "source": source_info,
            "context": context  # <--- Added this line
        }