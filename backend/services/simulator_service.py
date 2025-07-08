import pandas as pd
from simulator.simulator import AdvancedInventorySimulator
from simulator.google_sheets_connector import connect_to_sheet
import threading
import time
import os

simulator = AdvancedInventorySimulator('shared_assets/expanded_dataset_walmart_final_priced.csv')

# Simulation status tracking
global_simulation_status = {
    'status': 'idle',  # idle, running, completed, error
    'days_to_simulate': 0,
    'days_simulated': 0,
    'error': None
}
simulation_thread = None


def get_inventory_df():
    return simulator.get_dataframe()

def push_inventory_to_sheet(sheet_id: str) -> bool:
    try:
        sheet = connect_to_sheet(sheet_id)
        if sheet is None:
            return False
        sheet.clear()
        sheet_data = [simulator.df.columns.values.tolist()] + simulator.df.values.tolist()
        sheet.update(sheet_data)
        return True
    except Exception as e:
        print("Sheet Push Error:", e)
        return False

def _run_simulation(days: int):
    global global_simulation_status
    global_simulation_status['status'] = 'running'
    global_simulation_status['days_to_simulate'] = days
    global_simulation_status['days_simulated'] = 0
    global_simulation_status['error'] = None
    try:
        for i in range(days):
            if global_simulation_status['status'] != 'running':
                break
            simulator.simulate_day()
            global_simulation_status['days_simulated'] += 1
            time.sleep(0.1)  # Simulate time delay for realism
        if global_simulation_status['status'] == 'running':
            global_simulation_status['status'] = 'completed'
    except Exception as e:
        global_simulation_status['status'] = 'error'
        global_simulation_status['error'] = str(e)

def start_simulation(days: int):
    global simulation_thread
    if global_simulation_status['status'] == 'running':
        raise Exception('Simulation already running')
    simulation_thread = threading.Thread(target=_run_simulation, args=(days,))
    simulation_thread.start()
    return True

def stop_simulation():
    if global_simulation_status['status'] == 'running':
        global_simulation_status['status'] = 'stopped'
        return True
    return False

def get_simulation_status():
    return global_simulation_status.copy()

def get_forecast():
    """Get demand and sales forecast from Google Sheet inventory data"""
    # Get current inventory data from Google Sheet
    try:
        sheet = connect_to_sheet(os.getenv('SHEET_ID'))
        if sheet is None:
            return []
            
        # Get all rows including headers
        rows = sheet.get_all_values()
        if not rows or len(rows) < 2:
            return []
            
        # Convert to DataFrame
        df = pd.DataFrame(rows[1:], columns=rows[0])
        
        # Define required forecast columns
        required_columns = [
            'item_id', 
            'item_name',
            'predicted_daily_sales',
            'predicted_monthly_sales',
            'daily_sales', # Historical daily sales
            'elasticity'  # Price elasticity for demand forecasting
        ]
        
        # Check if required columns exist
        if not all(col in df.columns for col in required_columns):
            return []
            
        # Calculate forecasts based on historical sales and elasticity
        df['predicted_daily_sales'] = df['daily_sales'].astype(float) * (1 + df['elasticity'].astype(float))
        df['predicted_monthly_sales'] = df['predicted_daily_sales'] * 30
        
        # Extract forecast data
        forecast_df = df[required_columns]
        forecast = forecast_df.to_dict(orient='records')
        
        return forecast
        
    except Exception as e:
        print(f"Error getting forecast: {e}")
        return []
