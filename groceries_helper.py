import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    scope
)

client = gspread.authorize(creds)

sheet = client.open("Groceries List History").sheet1


def save_cart(shop, df):

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    for _, row in df.iterrows():

        sheet.append_row([
            now,
            shop,
            row["products"],
            row["quantity"]
        ])