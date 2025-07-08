from pydantic import BaseModel
from typing import Optional, Any

class InventoryItem(BaseModel):
    item_id: str
    item_name: str
    category: str
    department: str
    shelf_life_days: Any
    days_remaining: Any
    initial_stock: Any
    current_stock: Any
    base_price: Any
    dynamic_price: Any
    daily_sales: Any
    elasticity: Any
    restock_frequency_days: Any
    last_restock_date: str
    next_restock_date: str
    carbon_score: Any
    predicted_monthly_sales: Any
    predicted_daily_sales: Any
    days_until_restock: Any
    days_stock_lasts: Any

class InventoryCreate(BaseModel):
    item_id: str
    item_name: str
    category: str
    department: str
    shelf_life_days: Any
    days_remaining: Any
    initial_stock: Any
    current_stock: Any
    base_price: Any
    dynamic_price: Any
    daily_sales: Any
    elasticity: Any
    restock_frequency_days: Any
    last_restock_date: str
    next_restock_date: str
    carbon_score: Any
    predicted_monthly_sales: Any
    predicted_daily_sales: Any
    days_until_restock: Any
    days_stock_lasts: Any

class InventoryUpdate(BaseModel):
    item_name: Optional[str] = None
    category: Optional[str] = None
    department: Optional[str] = None
    shelf_life_days: Optional[Any] = None
    days_remaining: Optional[Any] = None
    initial_stock: Optional[Any] = None
    current_stock: Optional[Any] = None
    base_price: Optional[Any] = None
    dynamic_price: Optional[Any] = None
    daily_sales: Optional[Any] = None
    elasticity: Optional[Any] = None
    restock_frequency_days: Optional[Any] = None
    last_restock_date: Optional[str] = None
    next_restock_date: Optional[str] = None
    carbon_score: Optional[Any] = None
    predicted_monthly_sales: Optional[Any] = None
    predicted_daily_sales: Optional[Any] = None
    days_until_restock: Optional[Any] = None
    days_stock_lasts: Optional[Any] = None
