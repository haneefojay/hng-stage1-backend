from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import AnalyzedString
from typing import Dict, Any

async def get_by_value(session: AsyncSession, value: str) -> AnalyzedString | None:
    query = select(AnalyzedString).where(AnalyzedString.value == value)
    res = await session.execute(query)
    return res.scalars().first()

async def get_by_id(session: AsyncSession, id_:str) -> AnalyzedString | None:
    query = select(AnalyzedString).where(AnalyzedString.id == id_)
    res = await session.execute(query)
    return res.scalars().first()

async def create_string(session: AsyncSession, payload: Dict[str, Any]) -> AnalyzedString:
    obj = AnalyzedString(
        id=payload["properties"]["sha256_hash"],
        value=payload["value"],
        length=payload["properties"]["length"],
        is_palindrome=payload["properties"]["is_palindrome"],
        unique_characters=payload["properties"]["unique_characters"],
        word_count=payload["properties"]["word_count"],
        properties=payload["properties"]
    )
    
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

async def delete_by_value(session: AsyncSession, value: str) -> bool:
    obj = await get_by_value(session, value)
    if not obj:
        return False
    await session.delete(obj)
    await session.commit()
    return True

async def list_filtered(session: AsyncSession, filters: Dict[str, Any], limit: int = 100, offset: int = 0):
    query = select(AnalyzedString)
    conditions = []
    if "is_palindrome" in filters:
        conditions.append(AnalyzedString.is_palindrome == filters["is_palindrome"])
    if "min_length" in filters:
        conditions.append(AnalyzedString.length >= filters["min_length"])
    if "max_length" in filters:
        conditions.append(AnalyzedString.length <= filters["max_length"])
    if "word_count" in filters:
        conditions.append(AnalyzedString.word_count == filters["word_count"])
    if "contains_character" in filters:
        ch = filters["contains_character"]
        # use SQL JSONB containment or check properties->'character_frequency_map' ? keys. Simpler: text search on properties JSON
        conditions.append(AnalyzedString.properties["character_frequency_map"].has_key(ch))  # PostgreSQL specific
    if conditions:
        query = query.where(and_(*conditions))
    query = query.limit(limit).offset(offset)
    res = await session.execute(query)
    rows = res.scalars().all()
    return rows
