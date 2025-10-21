from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import ValidationError
from typing import Optional
from app.schema import StringCreate, StringResponse
from app.utils import analize_string, parse_nl_query
from app.database import get_session
from app import crud

router = APIRouter(prefix="/strings", tags=["Strings"])

@router.post("", status_code=201, response_model=StringResponse)
async def create_string_endpoint(payload: StringCreate, session=Depends(get_session)):
    try:
        val = payload.value
        if val is None or (isinstance(val, str) and not val.strip()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request body or missing 'value' field"
            )
        
        if not isinstance(val, str):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail='Invalid data type for "value" (must be string)'
            )
        
        existing = await crud.get_by_value(session, val)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="String already exists in the system"
            )
        
        props = analize_string(val)
        db_obj = await crud.create_string(session, {"value": val, "properties": props})
        
        return {
            "id": db_obj.id,
            "value": db_obj.value,
            "properties": db_obj.properties,
            "created_at": db_obj.created_at,
        }
    
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data type for "value" (must be string)'
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to process string: {str(e)}"
        )


@router.get("/filter-by-natural-language", response_model=dict)
async def filter_by_nl(query: str, session=Depends(get_session)):
    try:
        if not query or not query.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Query parameter 'query' is required and cannot be empty"
            )
        
        parsed = parse_nl_query(query)
        if not parsed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to parse natural language query"
            )
        
        if parsed.get("min_length_exclusive"):
            parsed["min_length"] = parsed["min_length_raw"] + 1
            parsed.pop("min_length_exclusive", None)
            parsed.pop("min_length_raw", None)
        
        rows = await crud.list_filtered(session, parsed)
        
        if not isinstance(rows, list):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Error processing query results"
            )

        data = [
            {
                "id": r.id,
                "value": r.value,
                "properties": r.properties,
                "created_at": r.created_at
            }
            for r in rows
        ]

        return {
            "data": data,
            "count": len(data),
            "interpreted_query": {"original": query, "parsed_filters": parsed}
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Failed to process query: {str(e)}"
        )


@router.get("/{string_value}", response_model=StringResponse)
async def get_string(string_value: str, session=Depends(get_session)):
    
    obj = await crud.get_by_value(session, string_value)
    if not obj:
        obj = await crud.get_by_id(session, string_value)
    
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="String does not exist in the system")
    
    return {
        "id": obj.id,
        "value": obj.value,
        "properties": obj.properties,
        "created_at": obj.created_at
    }

@router.get("", response_model=dict)
async def list_strings(
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None, ge=0),
    max_length: Optional[int] = Query(None, ge=0),
    word_count: Optional[int] = Query(None, ge=0),
    contains_character: Optional[str] = Query(None, min_length=1, max_length=1),
    session=Depends(get_session)
):
    try:
        if (
            (min_length is not None and not isinstance(min_length, int)) or
            (max_length is not None and not isinstance(max_length, int)) or
            (word_count is not None and not isinstance(word_count, int)) or
            (contains_character is not None and not isinstance(contains_character, str)) or
            (is_palindrome is not None and not isinstance(is_palindrome, bool))
        ):
            raise ValueError
        
        filters = {}
        if is_palindrome is not None:
            filters["is_palindrome"] = is_palindrome
        if min_length is not None:
            filters["min_length"] = min_length
        if max_length is not None:
            filters["max_length"] = max_length
        if word_count is not None:
            filters["word_count"] = word_count
        if contains_character is not None:
            filters["contains_character"] = contains_character
        
        rows = await crud.list_filtered(session, filters)
        data = [
            {
                "id": r.id,
                "value": r.value,
                "properties": r.properties,
                "created_at": r.created_at
            }
            for r in rows
        ]
        
        return {"data": data, "count": len(data), "filters_applied": filters}
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid query parameter values or types"
        )


@router.delete("/{string_value}", status_code=204)
async def delete_string(string_value: str, session=Depends(get_session)):
    string = await crud.delete_by_value(session, string_value)
    if not string:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="String does not exist in the system")
    return None