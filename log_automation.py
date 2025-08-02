import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_google_sheets(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("spheric-host-449612-v0-659c22ca76e4.json", scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name)

def log_to_google_sheet(sheet, df, tab_name):
    try:
        worksheet = sheet.worksheet(tab_name)
        sheet.del_worksheet(worksheet)
    except:
        pass
    worksheet = sheet.add_worksheet(title=tab_name, rows=str(len(df) + 1), cols=str(len(df.columns)))
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())