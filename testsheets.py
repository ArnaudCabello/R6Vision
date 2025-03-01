import gspread
from google.oauth2.service_account import Credentials
import subprocess

# Google Sheets authentication
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("creds.json", scopes=scopes)
client = gspread.authorize(creds)

# Google Sheet ID and sheet reference
sheet_id = "Sheet ID"
sheet = client.open_by_key(sheet_id).sheet1  # First sheet

# Run gemini.py and capture its output
process = subprocess.Popen(["python", "gemini.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = process.communicate()

if stderr:
    print("Error running gemini.py:", stderr)
    exit()

# Parse Gemini output
lines = stdout.strip().split("\n")
data = []

for line in lines:
    if "Player" in line:
        parts = line.split()  # Example: ["Player", "1:", "Resited", "16", "6", "2"]
        if len(parts) >= 5:
            name = " ".join(parts[2:-3])  # Combine everything except last 3 numbers
            kills = parts[-3]
            deaths = parts[-2]
            assists = parts[-1]
            data.append([name, kills, deaths, assists])

# Write data to Google Sheet
if data:
    sheet.append_rows(data, value_input_option="RAW")
    print("Data successfully written to Google Sheets!")
else:
    print("No valid player data found.")