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

sales = SHEET.worksheet('sales')
data = sales.get_all_values()[1:]
all_data = sales.get_all_values()

def get_weekly_sales():
    print('Getting sales for the week...\n')

    # Total sales
    total_sales = sum(int(row[1]) for row in data)
    print(f"Total sales for the week: {total_sales}$")
    
    # Average check
    average_receipt = total_sales / 7
    print(f"The average check: {round(average_receipt)}$")


def main():
    """ Run all program functions """
    get_weekly_sales()
    profit_data = calculate_profit()
    update_worksheet_column(profit_data)

main()





