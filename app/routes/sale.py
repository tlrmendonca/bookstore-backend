from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models.sale import Sale
from bson import ObjectId
from bson.errors import InvalidId

from ..db import db
from ..utils.utils import validate_object_id

router = APIRouter(prefix="/sales", tags=["sales"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_sale(sale: Sale) -> Sale:
    """Create a new sale in the database"""
    sale_dict = sale.model_dump(by_alias=True, exclude_none=True)
    sale_dict.pop("_id", None)

    result = await db.sales.insert_one(sale_dict)
    if not result.acknowledged:
        raise HTTPException(status_code=500, detail="Failed to create sale")

    sale_dict["_id"] = str(result.inserted_id)
    return Sale(**sale_dict)


@router.get("/{sale_id}")
async def get_sale(sale_id: str) -> Sale:
    """Get a single sale by its MongoDB ObjectId"""
    sale_object_id = validate_object_id(sale_id, "sale")

    sale_data = await db.sales.find_one({"_id": sale_object_id})
    if not sale_data:
        raise HTTPException(status_code=404, detail="Sale not found")

    sale_data["_id"] = str(sale_data["_id"])
    return Sale(**sale_data)


@router.get("/client/{client_id}")
async def get_sales_by_client(client_id: str) -> List[Sale]:
    """Get all sales for a specific client by their MongoDB ObjectId"""
    client_object_id = validate_object_id(client_id, "client")

    sales_data = await db.sales.find({"client_id": str(client_object_id)}).to_list(length=None)
    if not sales_data:
        raise HTTPException(status_code=404, detail="No sales found for this client")

    for sale in sales_data:
        sale["_id"] = str(sale["_id"])

    return [Sale(**sale) for sale in sales_data]


@router.get("/bookstore/{bookstore_id}")
async def get_sales_by_bookstore(bookstore_id: str) -> List[Sale]:
    """Get all sales for a specific bookstore by its MongoDB ObjectId"""
    bookstore_object_id = validate_object_id(bookstore_id, "bookstore")

    sales_data = await db.sales.find({"bookstore_id": str(bookstore_object_id)}).to_list(length=None)
    if not sales_data:
        raise HTTPException(status_code=404, detail="No sales found for this bookstore")

    for sale in sales_data:
        sale["_id"] = str(sale["_id"])

    return [Sale(**sale) for sale in sales_data]