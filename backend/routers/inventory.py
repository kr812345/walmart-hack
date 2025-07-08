from fastapi import APIRouter, HTTPException
from typing import List
from backend.services import inventory as inventory_service
from backend.schema.schema_inventory import InventoryItem, InventoryCreate, InventoryUpdate
from backend.services.recommendation import recommend_inventory_actions

router = APIRouter()

# Routes
@router.get("/inventory", response_model=List[InventoryItem])
def list_inventory():
    try:
        items = inventory_service.get_all_inventory()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inventory/{item_id}", response_model=InventoryItem)
def get_inventory(item_id: str):
    item = inventory_service.get_inventory_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/inventory", response_model=InventoryItem)
def create_inventory(item: InventoryCreate):
    try:
        inventory_service.create_inventory_item(item.dict())
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/inventory/{item_id}", response_model=InventoryItem)
def update_inventory(item_id: str, item: InventoryUpdate):
    existing = inventory_service.get_inventory_item(item_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    # Merge updates
    updated = {**existing, **{k: v for k, v in item.dict().items() if v is not None}}
    try:
        inventory_service.update_inventory_item(item_id, updated)
        return updated
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/inventory/{item_id}")
def delete_inventory(item_id: str):
    existing = inventory_service.get_inventory_item(item_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        inventory_service.delete_inventory_item(item_id)
        return {"message": "Item deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/inventory/classify")
def classify_inventory():
    try:
        items = inventory_service.get_all_inventory()
        classifications = inventory_service.classify_inventory_items(items)
        return {"classifications": classifications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/inventory/recommend")
def recommend_inventory():
    try:
        items = inventory_service.get_all_inventory()
        recommendations = recommend_inventory_actions(items)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 