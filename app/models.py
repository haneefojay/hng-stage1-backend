from sqlalchemy import Column, String, TIMESTAMP, func, Integer, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import text 
from app.database import Base



class AnalyzedString(Base):
    
    __tablename__ = "strings"
    
    id = Column(String(64), primary_key=True, index=True)
    value = Column(String, nullable=False, unique=True)
    length = Column(Integer, nullable=False)
    is_palindrome = Column(Boolean, nullable=False)
    unique_characters = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    properties = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)