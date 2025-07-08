from pydantic import BaseModel
from typing import Optional

class SimulationStartRequest(BaseModel):
    days: int

class SimulationStatusResponse(BaseModel):
    status: str
    days_to_simulate: int
    days_simulated: int
    error: Optional[str] = None

class ForecastItem(BaseModel):
    item_id: str
    item_name: str
    predicted_daily_sales: float
    predicted_monthly_sales: float 