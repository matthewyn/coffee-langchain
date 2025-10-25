from typing import List
from pydantic import BaseModel, Field

class StartingQuestion(BaseModel):
    """3 starting questions about coffee that a user might ask."""
    questions: List[str] = Field(
        description="A list of 3 questions about coffee that a user might ask.",
        min_items=3,
        max_items=3,
    )