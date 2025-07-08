from fastapi import APIRouter, HTTPException, Body
from backend.services.recommendation import recommend_inventory_actions, apply_recommendation
from backend.services.inventory import get_all_inventory

router = APIRouter()

@router.post("/recommend")
def recommend_inventory():
    try:
        items = get_all_inventory()
        recommendations = recommend_inventory_actions(items)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/apply-recommendation")
def apply_recommendation_api(
    item_id: str = Body(..., embed=True),
    recommendation: str = Body(..., embed=True)
):
    try:
        success = apply_recommendation(item_id, recommendation)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to apply recommendation")
        return {"message": f"Applied {recommendation} to item {item_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 