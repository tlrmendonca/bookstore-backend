from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId


def validate_object_id(id_str: str, entity_name: str = "object") -> ObjectId:
    """
    Validate and convert a string ID to MongoDB ObjectId.

    Raises: HTTPException: 400 status if ID format is invalid
    """
    try:
        return ObjectId(id_str)
    except InvalidId:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid {entity_name} ID format"
        )