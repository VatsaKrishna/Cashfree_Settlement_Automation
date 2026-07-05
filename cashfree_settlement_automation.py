import requests
import gspread
from google.oauth2.service_account import Credentials

from dotenv import load_dotenv
import os
load_dotenv()
CLIENT_ID = os.getenv("CASHFREE_CLIENT_ID")
CLIENT_SECRET = os.getenv("CASHFREE_CLIENT_SECRET")

from datetime import datetime, timedelta
today = datetime.now()

yesterday = today - timedelta(days=1)

formatted_date = yesterday.strftime("%Y-%m-%d")

start_date = f"{formatted_date}T00:00:00Z"
end_date = f"{formatted_date}T23:59:59Z"

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=scope
)

client = gspread.authorize(creds)

spreadsheet = client.open("MIMO Cashfree Settlements")
worksheet = spreadsheet.sheet1


existing_records = worksheet.get_all_values()

existing_ids = set()


for row in existing_records[1:]:
    if len(row) > 1:
        existing_ids.add(row[1])


url = "https://api.cashfree.com/pg/settlements"

headers = {
    "Content-Type": "application/json",
    "x-api-version": "2023-08-01",
    "x-client-id": CLIENT_ID,
    "x-client-secret": CLIENT_SECRET
}

body = {
    "product": "PG",
    "pagination": {
        "limit": 1000
    },
    "filters": {
        "start_date": start_date,
        "end_date": end_date
    }
}

response = requests.post(url=url, headers=headers, json=body)



if response.status_code != 200:
    print("API request failed")
    print("Status Code:", response.status_code)
    print("Response:", response.text)
    exit()

data = response.json()
settlements = data.get("data", [])


rows = []

for settlement in settlements:

    settlement_id = settlement.get("cf_settlement_id")


    if settlement_id in existing_ids:
        continue

    row = [
        settlement.get("settlement_date"),
        settlement.get("cf_settlement_id"),
        settlement.get("payment_amount"),
        settlement.get("amount_settled"),
        settlement.get("service_charge"),
        settlement.get("service_tax"),
        settlement.get("settlement_utr"),
        settlement.get("status")
    ]

    rows.append(row)


if rows:
    worksheet.append_rows(rows)
    print(f"{len(rows)} new settlements added.")
else:
    print("No new settlements found.")

