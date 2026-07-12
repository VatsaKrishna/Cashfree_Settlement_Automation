import requests
import gspread
from google.oauth2.service_account import Credentials

def format_section(sheet_id, row, red, green, blue):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": row,
                "endRowIndex": row + 1,
                "startColumnIndex": 0,
                "endColumnIndex": 4
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": red,
                        "green": green,
                        "blue": blue
                    },
                    "textFormat": {
                        "bold": True,
                        "fontSize": 11,
                        "foregroundColor": {
                            "red": 1,
                            "green": 1,
                            "blue": 1
                        }
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat)"
        }
    }

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

spreadsheet = client.open("MIMO Business Intelligence System")
settlements_sheet = spreadsheet.worksheet("Settlements")
dashboard_sheet = spreadsheet.worksheet("Dashboard")


existing_records = settlements_sheet.get_all_values()

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
print("Number of settlements:", len(settlements))
print(settlements)

payments = []

settled_amounts = []

service_charges = []

service_taxes = []

rows = []

for settlement in settlements:
    payment = settlement.get("payment_amount")
    print(payment)

    payments.append(payment)

    settled = settlement.get("amount_settled")
    print(settled)

    settled_amounts.append(settled)

    service_charge = settlement.get("service_charge") or 0
    service_tax = settlement.get("service_tax") or 0

    service_charges.append(service_charge)
    service_taxes.append(service_tax)

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
print("Payments List:", payments)
print("Settled List:", settled_amounts)

if len(payments) > 0:
    total_revenue = sum(payments)
    total_settled = sum(settled_amounts)

    number_of_orders = len(payments)

    highest_order = max(payments)
    lowest_order = min(payments)

    average_order = round(total_revenue / number_of_orders, 2)

    pending_amount = round(total_revenue - total_settled, 2)

    settlement_completion = round(
        (total_settled / total_revenue) * 100,
        2
    )

    pending_percentage = round(
        (pending_amount / total_revenue) * 100,
        2
    )

else:
    total_revenue = 0
    total_settled = 0

    number_of_orders = 0

    highest_order = 0
    lowest_order = 0

    average_order = 0

    pending_amount = 0

    settlement_completion = 0

    pending_percentage = 0

if number_of_orders == 0:
    system_status = "⚪ No Settlement Activity"

elif settlement_completion >= 95:
    system_status = "✅ Healthy"

elif settlement_completion >= 80:
    system_status = "⚠ Needs Attention"

else:
    system_status = "❌ Critical"

dashboard_data = [
    ["📊 MIMO EXECUTIVE DASHBOARD"],
    [""],
["📅 Last Updated", "", "", datetime.now().strftime("%d %b %Y")],
    ["🕒 Last Refresh", "", "", datetime.now().strftime("%I:%M %p")],
    [""],

    ["💰 DAILY SETTLEMENT PERFORMANCE", "", "", ""],
    ["Total Revenue", "", "", total_revenue],
    ["Amount Settled", "", "", total_settled],
    ["Service Charges", "", "", round(sum(service_charges), 2)],
    ["GST on Charges", "", "", round(sum(service_taxes), 2)],
    [""],

    ["📦 SETTLEMENT SUMMARY", "", "", ""],
    ["Number of Settlements", "", "", number_of_orders],
    ["Average Settlement Value", "", "", average_order],
    ["Highest Settlement", "", "", highest_order],
    ["Lowest Settlement", "", "", lowest_order],
    [""],

    ["📈 SETTLEMENT HEALTH", "", "", ""],
    ["Settlement Completion %", "", "", f"{settlement_completion}%"],
    ["Settlement Cost %", "", "", f"{pending_percentage}%"],
    ["System Status", "", "", system_status],

[""],
["────────────────────────────────────────────────────────────"],
["MBIS v2.1"],
["Developed by", "", "", "Vatsa Krishna Raj"],
["© 2026 Vision Printt Technologies LLP"]
]
dashboard_sheet.freeze(rows=1)
dashboard_sheet.columns_auto_resize(0, 2)
dashboard_sheet.clear()

dashboard_sheet.update(
    values=dashboard_data,
    range_name="A1"
)

spreadsheet.batch_update({
    "requests": [
        {
            "mergeCells": {
                "range": {
                    "sheetId": dashboard_sheet.id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 4
                },
                "mergeType": "MERGE_ALL"
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": dashboard_sheet.id,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 4
                },
                "cell": {
                    "userEnteredFormat": {
                        "horizontalAlignment": "CENTER",
                        "textFormat": {
                            "fontSize": 16,
                            "bold": True,
                            "foregroundColor": {
                                "red": 1,
                                "green": 1,
                                "blue": 1
                            }
                        },
                        "backgroundColor": {
                            "red": 0.09,
                            "green": 0.29,
                            "blue": 0.55
                        }
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
            }
        },
{
    "repeatCell": {
        "range": {
            "sheetId": dashboard_sheet.id,
            "startRowIndex": 4,
            "endRowIndex": 5,
            "startColumnIndex": 0,
            "endColumnIndex": 4
        },
        "cell": {
            "userEnteredFormat": {
                "backgroundColor": {
                    "red": 0.22,
                    "green": 0.63,
                    "blue": 0.29
                },
                "textFormat": {
                    "bold": True,
                    "foregroundColor": {
                        "red": 1,
                        "green": 1,
                        "blue": 1
                    }
                }
            }
        },
        "fields": "userEnteredFormat(backgroundColor,textFormat)"
    }
},
{
    "repeatCell": {
        "range": {
            "sheetId": dashboard_sheet.id,
            "startRowIndex": 10,
            "endRowIndex": 11,
            "startColumnIndex": 0,
            "endColumnIndex": 4
        },
        "cell": {
            "userEnteredFormat": {
                "backgroundColor": {
                    "red": 0.48,
                    "green": 0.29,
                    "blue": 0.69
                },
                "textFormat": {
                    "bold": True,
                    "foregroundColor": {
                        "red": 1,
                        "green": 1,
                        "blue": 1
                    }
                }
            }
        },
        "fields": "userEnteredFormat(backgroundColor,textFormat)"
    }
},
{
    "repeatCell": {
        "range": {
            "sheetId": dashboard_sheet.id,
            "startRowIndex": 16,
            "endRowIndex": 17,
            "startColumnIndex": 0,
            "endColumnIndex": 4
        },
        "cell": {
            "userEnteredFormat": {
                "backgroundColor": {
                    "red": 0.91,
                    "green": 0.49,
                    "blue": 0.13
                },
                "textFormat": {
                    "bold": True,
                    "foregroundColor": {
                        "red": 1,
                        "green": 1,
                        "blue": 1
                    }
                }
            }
        },
        "fields": "userEnteredFormat(backgroundColor,textFormat)"
    }
},
{
    "repeatCell": {
        "range": {
            "sheetId": dashboard_sheet.id,
            "startRowIndex": 5,
            "endRowIndex": 20,
            "startColumnIndex": 0,
            "endColumnIndex": 1
        },
        "cell": {
            "userEnteredFormat": {
                "textFormat": {
                    "bold": True
                }
            }
        },
        "fields": "userEnteredFormat.textFormat.bold"
    }
},
{
    "updateDimensionProperties": {
        "range": {
            "sheetId": dashboard_sheet.id,
            "dimension": "COLUMNS",
            "startIndex": 0,
            "endIndex": 1
        },
        "properties": {
            "pixelSize": 240
        },
        "fields": "pixelSize"
    }
},
{
    "updateDimensionProperties": {
        "range": {
            "sheetId": dashboard_sheet.id,
            "dimension": "COLUMNS",
            "startIndex": 3,
            "endIndex": 4
        },
        "properties": {
            "pixelSize": 160
        },
        "fields": "pixelSize"
    }
},
{
    "repeatCell": {
        "range": {
            "sheetId": dashboard_sheet.id,
            "startRowIndex": 5,
            "endRowIndex": 10,
            "startColumnIndex": 3,
            "endColumnIndex": 4
        },
        "cell": {
            "userEnteredFormat": {
                "numberFormat": {
                    "type": "CURRENCY",
                    "pattern": "₹#,##0.00"
                }
            }
        },
        "fields": "userEnteredFormat.numberFormat"
    }
},
{
    "repeatCell": {
        "range": {
            "sheetId": dashboard_sheet.id,
            "startRowIndex": 12,
            "endRowIndex": 15,
            "startColumnIndex": 3,
            "endColumnIndex": 4
        },
        "cell": {
            "userEnteredFormat": {
                "numberFormat": {
                    "type": "CURRENCY",
                    "pattern": "₹#,##0.00"
                }
            }
        },
        "fields": "userEnteredFormat.numberFormat"
    }
},
{
    "repeatCell": {
        "range": {
            "sheetId": dashboard_sheet.id,
            "startRowIndex": 11,
            "endRowIndex": 12,
            "startColumnIndex": 3,
            "endColumnIndex": 4
        },
        "cell": {
            "userEnteredFormat": {
                "numberFormat": {
                    "type": "NUMBER",
                    "pattern": "0"
                }
            }
        },
        "fields": "userEnteredFormat.numberFormat"
    }
},

    ]
})

print("Dashboard updated successfully!")

if rows:
    settlements_sheet.append_rows(rows)
    print(f"{len(rows)} new settlements added.")
else:
    print("No new settlements found.")

