import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('apple_sales')

# sales = SHEET.worksheet('sales')
# data = sales.get_all_values()
# print(data)

def get_total_sales():
    print('Calculating total sales for the week...\n')
    sales = SHEET.worksheet('sales')
    sales_data = sales.get_all_values()

    total_sales = sum(int(row[1]) for row in sales_data[1:])
    print(f"Total sales for the week: {total_sales}")
    
get_total_sales()