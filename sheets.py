import gspread
from google.oauth2.service_account import Credentials
import sys

# Google Sheets authentication
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("creds.json", scopes=scopes)
client = gspread.authorize(creds)

# Google Sheet ID and sheet reference
sheet_id = "Sheet ID"
sheet = client.open_by_key(sheet_id).sheet1  # First sheet

# Read processed Gemini output from stdin
gemini_output = sys.stdin.read()
if not gemini_output:
    print("Error: No data received from Gemini.")
    sys.exit(1)

# Parse Gemini output
lines = gemini_output.split("\n")
data = []

for line in lines:
    if "Player" in line:
        parts = line.split()
        if len(parts) >= 5:
            name = " ".join(parts[2:-3])  # Extract name
            kills, deaths, assists = parts[-3], parts[-2], parts[-1]  # Extract stats
            data.append([name, kills, deaths, assists])

# Write data to Google Sheets
if data:
    sheet.append_rows(data, value_input_option="RAW")
    print("Data successfully written to Google Sheets!")
else:
    print("No valid player data found.")