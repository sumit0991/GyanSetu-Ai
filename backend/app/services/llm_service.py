from langchain_google_genai import ChatGoogleGenerativeAI
from backend.app.core.config import settings
import logging

# Set up logging to see errors in your terminal clearly
logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        # We use Gemini 3 Flash (the 2026 standard) or 2.5 Flash as a fallback.
        # These are much faster and more reliable than the legacy 1.5 version.
        self.primary_model = "gemini-3-flash"
        self.fallback_model = "gemini-2.5-flash"

        self.llm = self._create_llm(self.primary_model)

    def _create_llm(self, model_name: str):
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.3,
            max_output_tokens=4096,
            # Explicitly using 'v1' instead of 'v1beta' avoids the 404 error
            version="v1"
        )

    def generate_exam_notes(self, structured_instruction: str, context: str):
        prompt = [
            ("system", "You are an Expert University Professor specializing in structured exam notes."),
            ("human", f"TEXTBOOK CONTEXT:\n{context}\n\nSTUDENT REQUEST:\n{structured_instruction}")
        ]

        try:
            # Attempt with Primary Model (Gemini 3 Flash)
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            logger.warning(f"Primary model {self.primary_model} failed. Trying fallback. Error: {e}")

            try:
                # Fallback attempt (Gemini 2.5 Flash)
                fallback_llm = self._create_llm(self.fallback_model)
                response = fallback_llm.invoke(prompt)
                return response.content
            except Exception as final_error:
                logger.error(f"All models failed: {final_error}")
                return f"<b>System Error:</b> Could not connect to Gemini API. Please check your API key and Internet connection.<br>Details: {str(final_error)}"