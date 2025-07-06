from google_sheets_connector import connect_to_sheet_by_id

class AdvancedInventorySimulator:
    # Your existing methods ...

    def push_to_google_sheet(self, sheet_id):
        sheet = connect_to_sheet_by_id(sheet_id)

        # Prepare headers and data
        sheet_data = [self.df.columns.values.tolist()] + self.df.values.tolist()

        sheet.update(sheet_data)
        print(f"Live data pushed to Google Sheet: {sheet_id}")
