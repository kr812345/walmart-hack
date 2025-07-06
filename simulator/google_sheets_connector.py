import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheet(sheet_id, creds_path='credentials/credentials.json'):
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)

        # Correct usage: open by key, not by title
        sheet = client.open_by_key(sheet_id).sheet1
        print(f"✅ Successfully connected to Google Sheet: {sheet.title}")
        return sheet

    except Exception as e:
        print(f"❌ Failed to connect to Google Sheet: {e}")
        return None

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# def connect_to_sheet_by_id(sheet_id, creds_path='credentials/credential.json'):
#     scope = [
#         'https://spreadsheets.google.com/feeds',
#         'https://www.googleapis.com/auth/spreadsheets',
#         'https://www.googleapis.com/auth/drive'
#     ]

#     creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
#     client = gspread.authorize(creds)

#     sheet = client.open_by_key(sheet_id).sheet1
#     return sheet
