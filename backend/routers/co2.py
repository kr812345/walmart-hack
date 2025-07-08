from fastapi import APIRouter, HTTPException
from backend.services.co2 import calculate_waste_co2, calculate_logistics_co2, calculate_total_co2
from backend.services.inventory import get_all_inventory

router = APIRouter()

@router.get("/co2/waste")
def co2_waste():
    try:
        items = get_all_inventory()
        result = calculate_waste_co2(items)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/co2/logistics")
def co2_logistics():
    try:
        items = get_all_inventory()
        result = calculate_logistics_co2(items)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/co2/total")
def co2_total():
    try:
        items = get_all_inventory()
        result = calculate_total_co2(items)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 