EMISSION_FACTOR_WASTE = 2.5  # kg CO2 per unit wasted
EMISSION_FACTOR_LOGISTICS = 0.5  # kg CO2 per unit per restock

def calculate_waste_co2(items):
    total = 0.0
    breakdown = []
    for item in items:
        try:
            if int(item.get('days_remaining', 0)) == 0:
                qty = int(item.get('current_stock', 0))
                co2 = qty * EMISSION_FACTOR_WASTE
                breakdown.append({'item_id': item.get('item_id'), 'item_name': item.get('item_name'), 'waste_co2': co2})
                total += co2
        except Exception:
            continue
    return {'total_waste_co2': total, 'breakdown': breakdown}

def calculate_logistics_co2(items):
    total = 0.0
    breakdown = []
    for item in items:
        try:
            restock_freq = int(item.get('restock_frequency_days', 0))
            qty = int(item.get('current_stock', 0))
            co2 = restock_freq * qty * EMISSION_FACTOR_LOGISTICS
            breakdown.append({'item_id': item.get('item_id'), 'item_name': item.get('item_name'), 'logistics_co2': co2})
            total += co2
        except Exception:
            continue
    return {'total_logistics_co2': total, 'breakdown': breakdown}

def calculate_total_co2(items):
    waste = calculate_waste_co2(items)['total_waste_co2']
    logistics = calculate_logistics_co2(items)['total_logistics_co2']
    return {'total_co2': waste + logistics, 'waste_co2': waste, 'logistics_co2': logistics} 