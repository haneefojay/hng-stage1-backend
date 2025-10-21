from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
from datetime import datetime

class StringCreate(BaseModel):
    value: str = Field(..., min_length=1)


class Properties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]

class StringResponse(BaseModel):
    id: str
    value: str
    properties: Properties
    created_at: Optional[datetime]