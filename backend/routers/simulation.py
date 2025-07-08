from fastapi import APIRouter, HTTPException
from typing import List
from backend.schema.schema_simulation import SimulationStartRequest, SimulationStatusResponse, ForecastItem
from backend.services import simulator_service
from simulator.simulator import AdvancedInventorySimulator as simulator
from backend.services.simulator_service import simulator, get_inventory_df, push_inventory_to_sheet

router = APIRouter()

# Routes
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

@router.post("/simulation/start")
def start_simulation(req: SimulationStartRequest):
    try:
        simulator_service.start_simulation(req.days)
        return {"message": f"Simulation started for {req.days} days"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/simulation/stop")
def stop_simulation():
    stopped = simulator_service.stop_simulation()
    if stopped:
        return {"message": "Simulation stopped"}
    else:
        raise HTTPException(status_code=400, detail="No simulation is running")

@router.get("/simulation/status", response_model=SimulationStatusResponse)
def get_simulation_status():
    status = simulator_service.get_simulation_status()
    return status

@router.get("/forecast", response_model=List[ForecastItem])
def get_forecast():
    forecast = simulator_service.get_forecast()
    return forecast