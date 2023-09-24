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

    # Maximum and minimum sales: 
    max_sales_day = max(data,  key=lambda x: int(x[1]))
    min_sales_day = min(data,  key=lambda x: int(x[1]))
    print(f"A day with maximum sales {max_sales_day[0]}, sales: {max_sales_day[1]}$")
    print(f"A day with minimum sales {min_sales_day[0]}, sales: {min_sales_day[1]}$")

def calculate_profit():
    """ 
    'Profit' - difference between sales and cost of sales 
    """
    profit = []
    for row in data:
        profit.append(int(row[1]) - int(row[3]))
    profit.insert(0, 'Profit')
   
    return profit


def main():
    """ Run all program functions """
    get_weekly_sales()
    profit_data = calculate_profit()
    update_worksheet_column(profit_data)

main()





