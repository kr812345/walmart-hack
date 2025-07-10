import pandas as pd
import random
from datetime import datetime, timedelta
from .google_sheets_connector import connect_to_sheet

class AdvancedInventorySimulator:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.current_date = datetime.now().date()

    def simulate_day(self):
        print(f"Simulating inventory for {self.current_date}...")

        for idx, row in self.df.iterrows():
            if row['current_stock'] <= 0 or row['days_remaining'] <= 0:
                continue  # Skip out-of-stock or expired items

            # Simulate weekday/weekend demand fluctuation
            demand_multiplier = 1.2 if self.current_date.weekday() in [5, 6] else 1.0
            base = row['base_price']
            elasticity = row['elasticity']
            predicted_daily_sales = row['predicted_daily_sales']
            base_sales = predicted_daily_sales * demand_multiplier
            elasticity_factor = (1 - (row['dynamic_price'] - base) / base) * elasticity

            sales_today = max(1, int(base_sales + random.uniform(-5, 5) + elasticity_factor * base_sales))
            sales_today = min(sales_today, row['current_stock'])

            self.df.at[idx, 'current_stock'] -= sales_today
            self.df.at[idx, 'daily_sales'] = sales_today

            # Shelf-life countdown
            self.df.at[idx, 'days_remaining'] = max(row['days_remaining'] - 1, 0)

            # Expired items
            if self.df.at[idx, 'days_remaining'] == 0 and self.df.at[idx, 'current_stock'] > 0:
                print(f"Item expired: {row['item_name']}, Stock wasted: {self.df.at[idx, 'current_stock']}")

            # Restocking if due
            if self.df.at[idx, 'days_until_restock'] <= 0:
                delivery_delay = random.choice([0, 1, 2])  # Random delivery delay
                restock_quantity = row['initial_stock']
                self.df.at[idx, 'current_stock'] += restock_quantity
                self.df.at[idx, 'days_until_restock'] = row['restock_frequency_days'] + delivery_delay
                self.df.at[idx, 'last_restock_date'] = self.current_date.strftime('%Y-%m-%d')
                self.df.at[idx, 'next_restock_date'] = (
                    self.current_date + timedelta(days=int(self.df.at[idx, 'days_until_restock']))
                ).strftime('%Y-%m-%d')
            else:
                self.df.at[idx, 'days_until_restock'] -= 1

            # ✅ Recalculate dynamic pricing AFTER sales and shelf update
            current_stock = self.df.at[idx, 'current_stock']
            days_remaining = self.df.at[idx, 'days_remaining']
            floor = base - elasticity

            if predicted_daily_sales > 0 and days_remaining > 0:
                predicted_remaining_sales = predicted_daily_sales * days_remaining
                stock_ratio = current_stock / predicted_remaining_sales

                if stock_ratio > 1.2:
                    discount = elasticity * 0.8
                    new_price = round(max(base - discount, floor), 2)
                    self.df.at[idx, 'dynamic_price'] = new_price
                else:
                    self.df.at[idx, 'dynamic_price'] = base
            else:
                self.df.at[idx, 'dynamic_price'] = base

            # 🔻 Additional markdown for nearly expired products
            if days_remaining <= 2 and current_stock > 0:
                reduced_price = round(self.df.at[idx, 'dynamic_price'] * 0.90, 2)
                self.df.at[idx, 'dynamic_price'] = max(reduced_price, base * 0.5)

        self.current_date += timedelta(days=1)

    def save_simulation(self, output_path):
        self.df.to_csv(output_path, index=False)
        print(f"Simulation updated and saved to {output_path}.")

    def get_dataframe(self):
        return self.df

    def push_to_google_sheet(self, sheet_id, creds_path='shared_assets/credentials/credentials.json'):
        sheet = connect_to_sheet(sheet_id, creds_path=creds_path)
        if sheet is None:
            print("❌ Could not push to Google Sheet: connection failed.")
            return

        # Prepare headers and data
        sheet_data = [self.df.columns.values.tolist()] + self.df.values.tolist()
        sheet.update(sheet_data)
        print(f"Live data pushed to Google Sheet: {sheet_id}")
