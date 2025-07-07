import pandas as pd
from simulator.simulator import AdvancedInventorySimulator
from simulator.google_sheets_connector import connect_to_sheet

simulator = AdvancedInventorySimulator('shared_assets/expanded_dataset_walmart_final_priced.csv')

def get_inventory_df():
    return simulator.get_dataframe()

def push_inventory_to_sheet(sheet_id: str) -> bool:
    try:
        sheet = connect_to_sheet(sheet_id)
        sheet.clear()
        sheet_data = [simulator.df.columns.values.tolist()] + simulator.df.values.tolist()
        sheet.update(sheet_data)
        return True
    except Exception as e:
        print("Sheet Push Error:", e)
        return False
