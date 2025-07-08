from backend.services.inventory import get_inventory_item, update_inventory_item, DEFAULT_SHEET_ID, DEFAULT_CREDS_PATH

def recommend_inventory_actions(items):
    """Recommend actions for inventory items: discount, restock, remove, or none."""
    results = []
    for item in items:
        try:
            days_remaining = int(item.get('days_remaining', 0))
            current_stock = int(item.get('current_stock', 0))
        except Exception:
            results.append({
                'item_id': item.get('item_id'),
                'item_name': item.get('item_name'),
                'recommendation': 'unknown'
            })
            continue
        if current_stock < 5:
            recommendation = 'restock'
        elif days_remaining < 3 and current_stock > 0:
            recommendation = 'discount'
        elif days_remaining == 0:
            recommendation = 'remove'
        else:
            recommendation = 'none'
        results.append({
            'item_id': item.get('item_id'),
            'item_name': item.get('item_name'),
            'recommendation': recommendation
        })
    return results

def apply_recommendation(item_id, recommendation, sheet_id=DEFAULT_SHEET_ID, creds_path=DEFAULT_CREDS_PATH):
    item = get_inventory_item(item_id, sheet_id, creds_path)
    if not item:
        return False
    updated = item.copy()
    if recommendation == 'restock':
        updated['current_stock'] = updated.get('initial_stock', updated.get('current_stock', 0))
    elif recommendation == 'discount':
        try:
            price = float(updated.get('dynamic_price', 0))
            updated['dynamic_price'] = str(round(price * 0.9, 2))
        except Exception:
            pass
    elif recommendation == 'remove':
        updated['current_stock'] = '0'
    else:
        return False
    return update_inventory_item(item_id, updated, sheet_id, creds_path) 