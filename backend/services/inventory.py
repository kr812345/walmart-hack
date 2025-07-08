from simulator.google_sheets_connector import connect_to_sheet
from typing import List, Dict, Any, Optional
import copy
import pandas as pd

# Default config (can be overridden in function calls)
DEFAULT_SHEET_ID = '1bpKO6Zo8ce8iVykC7TSWwteSFYujJBJY1wv2hffHcMI'  # TODO: Replace with actual sheet ID or pass as argument
DEFAULT_CREDS_PATH = 'shared_assets/credentials/credentials.json'

# The columns in the inventory sheet (must match the sheet header exactly)
INVENTORY_COLUMNS = [
    'item_id', 'item_name', 'category', 'department', 'shelf_life_days', 'days_remaining',
    'initial_stock', 'current_stock', 'base_price', 'dynamic_price', 'daily_sales', 'elasticity',
    'restock_frequency_days', 'last_restock_date', 'next_restock_date', 'carbon_score',
    'predicted_monthly_sales', 'predicted_daily_sales', 'days_until_restock', 'days_stock_lasts'
]

def get_all_inventory(sheet_id: str = DEFAULT_SHEET_ID, creds_path: str = DEFAULT_CREDS_PATH) -> List[Dict[str, Any]]:
    sheet = connect_to_sheet(sheet_id, creds_path)
    if sheet is None:
        raise Exception('Could not connect to Google Sheet')
    rows = sheet.get_all_values()
    if not rows or len(rows) < 2:
        return []
    header = rows[0]
    items = [dict(zip(header, row)) for row in rows[1:]]
    return items

def get_inventory_item(item_id: str, sheet_id: str = DEFAULT_SHEET_ID, creds_path: str = DEFAULT_CREDS_PATH) -> Optional[Dict[str, Any]]:
    items = get_all_inventory(sheet_id, creds_path)
    for item in items:
        if item.get('item_id') == item_id:
            return item
    return None

def create_inventory_item(item_data: Dict[str, Any], sheet_id: str = DEFAULT_SHEET_ID, creds_path: str = DEFAULT_CREDS_PATH) -> bool:
    sheet = connect_to_sheet(sheet_id, creds_path)
    if sheet is None:
        raise Exception('Could not connect to Google Sheet')
    # Ensure all columns are present
    row = [str(item_data.get(col, '')) for col in INVENTORY_COLUMNS]
    sheet.append_row(row)
    return True

def update_inventory_item(item_id: str, item_data: Dict[str, Any], sheet_id: str = DEFAULT_SHEET_ID, creds_path: str = DEFAULT_CREDS_PATH) -> bool:
    sheet = connect_to_sheet(sheet_id, creds_path)
    if sheet is None:
        raise Exception('Could not connect to Google Sheet')
    rows = sheet.get_all_values()
    if not rows or len(rows) < 2:
        return False
    header = rows[0]
    for idx, row in enumerate(rows[1:], start=2):  # 1-based index, skip header
        row_dict = dict(zip(header, row))
        if row_dict.get('item_id') == item_id:
            # Prepare updated row
            updated_row = [str(item_data.get(col, row_dict.get(col, ''))) for col in INVENTORY_COLUMNS]
            sheet.update([updated_row], f'A{idx}:T{idx}')
            return True
    return False

def delete_inventory_item(item_id: str, sheet_id: str = DEFAULT_SHEET_ID, creds_path: str = DEFAULT_CREDS_PATH) -> bool:
    sheet = connect_to_sheet(sheet_id, creds_path)
    if sheet is None:
        raise Exception('Could not connect to Google Sheet')
    rows = sheet.get_all_values()
    if not rows or len(rows) < 2:
        return False
    header = rows[0]
    for idx, row in enumerate(rows[1:], start=2):  # 1-based index, skip header
        row_dict = dict(zip(header, row))
        if row_dict.get('item_id') == item_id:
            sheet.delete_rows(idx)
            return True
    return False

def pull_inventory_as_dataframe(sheet_id: str = DEFAULT_SHEET_ID, creds_path: str = DEFAULT_CREDS_PATH):
    """Pull inventory from Google Sheet and return as a pandas DataFrame."""
    sheet = connect_to_sheet(sheet_id, creds_path)
    if sheet is None:
        raise Exception('Could not connect to Google Sheet')
    rows = sheet.get_all_values()
    if not rows or len(rows) < 2:
        return None
    columns = [str(col) for col in rows[0]]
    df = pd.DataFrame(rows[1:], columns=pd.Index(columns))
    return df

def classify_inventory_items(items):
    """Classify inventory items for return, donate, discard, or keep based on rules."""
    results = []
    for item in items:
        try:
            days_remaining = int(item.get('days_remaining', 0))
            current_stock = int(item.get('current_stock', 0))
            initial_stock = int(item.get('initial_stock', 0))
        except Exception:
            results.append({
                'item_id': item.get('item_id'),
                'item_name': item.get('item_name'),
                'classification': 'unknown'
            })
            continue
        if days_remaining == 0:
            classification = 'discard'
        elif current_stock > 0 and days_remaining < 3:
            classification = 'donate'
        elif current_stock > initial_stock:
            classification = 'return'
        else:
            classification = 'keep'
        results.append({
            'item_id': item.get('item_id'),
            'item_name': item.get('item_name'),
            'classification': classification
        })
    return results
