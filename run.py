import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
import pandas as pd

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

def get_total_sales():
    print('Getting sales for the week...\n')
    total_sales = sum(int(row[1]) for row in data)
    print(f"Total sales for the week: {total_sales}$")
    
    return total_sales

def get_average_check(total_sales):
    average_check = round(total_sales / 7)
    print(f"The average check: {round(average_check)}$")

    return average_check

def get_maximum_sales():
    max_sales_day = max(data,  key=lambda x: int(x[1]))
    print(f"A day with maximum sales {max_sales_day[0]}, sales: {max_sales_day[1]}$")
    
    return max_sales_day

def get_minimum_sales():
    min_sales_day = min(data,  key=lambda x: int(x[1]))
    print(f"A day with minimum sales {min_sales_day[0]}, sales: {min_sales_day[1]}$\n")

    return min_sales_day

def calculate_data(name):
    """
    Calculate specific metrics based on the provided 'name' using the given data, generates a list, 
    adds a header to the beginning and return calculated array.
    """
    data_array = [] 
    for row in data:
        daily_sales, customers, cost, ad_budget, orders = map(float, row[1:6])
        if name == 'profit':
            value = daily_sales - cost
            label = 'Profit'
        elif name == 'average_check':
            value = round(daily_sales / orders, 2)
            label = 'Average check'
        elif name == 'conversion_rate':
            value = round(orders / customers, 2)
            label = 'Conversion rate'

        data_array.append(value)
    data_array.insert(0, label)    
    
    return data_array

def calculate_roi():
    # Calculate Return on Investment

    roi_array = [] 
    update_data = sales.get_all_values()[1:]
    for row in update_data:
        ad_budget, profit = map(float, row[5:7])
        roi = round((profit - ad_budget) / ad_budget, 2)
        roi_array.append(roi)
    roi_array.insert(0, 'ROI (Return on Investment)')

    return roi_array

def main():
    """ Run all program functions """
    total_sales = get_total_sales()
    average_check = get_average_check(total_sales)
    max_sales = get_maximum_sales()
    min_sales = get_minimum_sales()

main()


