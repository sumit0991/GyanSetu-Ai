from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    """
    Note: While we are now using Form data for the main endpoint,
    keeping this schema ensures compatibility with other JSON-based tools.
    """
    subject: str = "DBMS"
    topics: str  # Changed from topic to topics to match current project logic
    num_marks: Optional[int] = 5


class QueryResponse(BaseModel):
    """
    Standard response structure for the Intelligent-Notes Engine.
    """
    topic: str  # This corresponds to the topics string sent by the user
    answer: str  # This contains the fully rendered HTML UI string

    # Optional fields for direct video access if needed by other services
    video_url: Optional[str] = None
    video_title: Optional[str] = None