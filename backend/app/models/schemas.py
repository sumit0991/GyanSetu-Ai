from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    subject: str
    topic: str

class QueryResponse(BaseModel):
    status: str
    answer: str
    source_nodes: Optional[List[dict]] = None