import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from tabulate import tabulate

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

def get_weekly_average_check(total_sales):
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

def calculate_mounthly_data(name):
    data_array = []

    for row in data:
        date = row[0]
        daily_sales, customers, cost, orders, ad_budget, profit,  = [float(x) for x in row[1:7]]
        if name == 'Profit':
            value = daily_sales - cost
            label = '$'
        elif name == 'Order average check':
            value = round(daily_sales / orders, 2)
            label = '$'
        elif name == 'Сonversion rate':
            value = orders / customers * 100
            label = '%'

        data_array.append([date, round(value, 2)])
    print(f'Getting {name} for the month...\n')
    print(tabulate(data_array, headers=["Date", f"{name} ({label})"], tablefmt="pretty"))

    return data_array

def calculate_roi():
    # Calculate Return on Investment

    roi_array = [] 
    update_data = sales.get_all_values()[1:]
    for row in update_data:
        ad_budget, profit = map(float, row[5:7])
        roi = round((profit - ad_budget) / ad_budget * 100, 2)
        roi_array.append([row[0], roi])
    print(f'Getting ROI for the month...\n')
    print(tabulate(roi_array, headers=["Date", "ROI (Return on Investment) %"], tablefmt="pretty"))
    
    return roi_array

def start_calculations():
    while True:
        print("Select an option:")
        print("1. Get monthly calculations")
        print("2. Get weekly calculations")
        print("3. Get daily calculations")
        print("4. Back to the main menu")
        
        choice = input("Enter the option number: ")
        
        if choice == "1":
            # Here will be the code for the monthly calculations
            get_monthly_calculations()
            print("")
        elif choice == "2":
            # Here will be the code for the weekly calculations
            print("")
        elif choice == "3":
            # Here will be the code for the daily calculations
            print("")
        elif choice == "4":
            break
        else:
            print("Некорректный выбор. Попробуйте еще раз.")

def show_about():
    print("Future description")

def get_monthly_calculations():
    while True:
        print("Select an option:")
        print("1. Get FULL REPORT")
        print("2. Get total sales")
        print("3. Get weekly average check")
        print("4. Get maximum sales")
        print("5. Get minimum sales")
        print("6. Get profit")
        print("7. Get order average check")
        print("8. Get conversion rate")
        print("9. Get ROI (Return on Investment)")
        print("10. Back")
        
        choice = input("Enter the option number: ")
        
        if choice == "1":
            # Here will be the code for the monthly calculations
            get_full_monthly_report()
        elif choice == "2":
            get_total_sales()

def get_full_monthly_report():
    print('Future code for monthly report')

def main():
    while True:
        print("Select an option:")
        print("1. Start calculations")
        print("2. About")
        print("3. End program")
        
        choice = input("Enter an option number: ")
        
        if choice == "1":
            start_calculations()
        elif choice == "2":
            show_about()
        elif choice == "3":
            break
        else:
            print("Incorrect selection. Try again.\n")

main()