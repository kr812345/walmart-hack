from fastapi import APIRouter, HTTPException
from simulator.advanced_simulatorsimulator import AdvancedInventorySimulator
from services.simulator_service import simulator, get_inventory_df, push_inventory_to_sheet

router = APIRouter()

@router.post("/simulate-day")
def simulate_day():
    simulator.simulate_day()
    return {"message": "Day simulated successfully"}

@router.get("/get-live-inventory")
def get_inventory():
    df = get_inventory_df()
    return {"inventory": df.to_dict(orient="records")}

@router.post("/push-to-sheet")
def push_to_sheet():
    success = push_inventory_to_sheet("your_google_sheet_id_here") # Replace with your actual sheet ID
    if not success:
        raise HTTPException(status_code=500, detail="Failed to push to sheet")
    return {"message": "Inventory pushed to Google Sheet"}