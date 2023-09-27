import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
import sys
import os

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

def validate_data(input_value, min_value, max_value):
    try:
        value = int(input_value)
        if min_value <= value <= max_value:
            return True
        else:
            print(f"\033[1mInput must be a number between {min_value} and {max_value}.\033[0m")
            return False
    except ValueError:
        print("\033[1mInput must be a number.\033[0m")
        return False


def get_total_sales():
    print('\033[1mGetting sales...\033[0m\n')
    total_sales = sum(int(row[1]) for row in data)
    print(f"\033[1mTotal sales: {total_sales}$\033[0m\n")
    
    return total_sales

def get_average_check(total_sales, days):
    print('\033[1mGetting average check...\033[0m\n')
    average_check = round(total_sales / days)
    print(f"\033[1mThe average check: {round(average_check)}$\033[0m\n")

    return average_check

def get_maximum_sales():
    max_sales_day = max(data,  key=lambda x: int(x[1]))
    print(f"\033[1mA day with maximum sales {max_sales_day[0]}, sales: {max_sales_day[1]}$\033[0m\n")
    
    return max_sales_day

def get_minimum_sales():
    min_sales_day = min(data,  key=lambda x: int(x[1]))
    print(f"\033[1mA day with minimum sales {min_sales_day[0]}, sales: {min_sales_day[1]}$\033[0m\n")

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
    print(f'\033[1mGetting {name} for the month...\033[0m\n')
    print(tabulate(data_array, headers=["Date", f"{name} ({label})"], tablefmt="pretty"))
    print()

    return data_array

def calculate_roi():
    # Calculate Return on Investment

    roi_array = [] 
    update_data = sales.get_all_values()[1:]
    for row in update_data:
        ad_budget, profit = map(float, row[5:7])
        roi = round((profit - ad_budget) / ad_budget * 100, 2)
        roi_array.append([row[0], roi])
    print(f'\033[1mGetting ROI for the month...\033[0m\n')
    print(tabulate(roi_array, headers=["Date", "ROI (Return on Investment) %"], tablefmt="pretty"))
    
    return roi_array

"""
------------------------------------------- Start all calculations -------------------------------------------
"""

def start_calculations():
    while True:
        print("Select an option:")
        print("1. Get monthly calculations")
        print("2. Get weekly calculations")
        print("3. Get daily data")
        print("4. Back to the main menu")
        print("5. End program")
        
        choice = int(input("Enter the option number: "))
        print()

        if validate_data(choice, 1, 5):
            choice = int(choice)
            if choice == 1:
                get_monthly_calculations()
            elif choice == 2:
                input_week = int(input("Enter the week number (1, 2, 3, or 4): "))
                if validate_data(input_week, 1, 4):
                    input_week = int(input_week)
                    get_weekly_calculations(input_week, all_data)
            elif choice == 3:
                input_day = int(input("Enter the date (in the format DD): "))
                if validate_data(input_day, 1, 30):
                    input_day = int(input_day)
                    get_daily_data(input_day, data)
            elif choice == 4:
                break
            elif choice == 5:
                sys.exit()
            else:
                print("Incorrect selection. Try again.\n")

"""
------------------------------------------- Mounthly calculations -------------------------------------------
"""

def get_monthly_calculations():
    total_sales = 0
    while True:
        print("Select an option:")
        print("1. Get FULL REPORT")
        print("2. Get total sales")
        print("3. Get monthly average check")
        print("4. Get maximum sales")
        print("5. Get minimum sales")
        print("6. Get profit")
        print("7. Get order average check")
        print("8. Get conversion rate")
        print("9. Get ROI (Return on Investment)")
        print("10. Back")
        print("11. End program")
        
        choice = int(input("Enter the option number: "))
        print()
        
        if validate_data(choice, 1, 11):
            choice = int(choice)
            if choice == 1:
                get_full_monthly_report()
            elif choice == 2:
                total_sales = get_total_sales()
            elif choice == 3:
                get_average_check(total_sales, 30)
            elif choice == 4:
                get_maximum_sales()
            elif choice == 5:
                get_minimum_sales()
            elif choice == 6:
                calculate_mounthly_data('Profit')
            elif choice == 7:
                calculate_mounthly_data('Order average check')
            elif choice == 8:
                calculate_mounthly_data('Сonversion rate')
            elif choice == 9:
                calculate_roi()
            elif choice == 10:
                break
            elif choice == 11:
                sys.exit()
            else:
                print("Incorrect selection. Try again.\n")

def get_full_monthly_report():
    total_sales = get_total_sales()
    get_average_check(total_sales, 30)
    get_maximum_sales()
    get_minimum_sales()
    table = tabulate(data, headers=all_data[0], tablefmt="simple")
    print(table)

"""
------------------------------------------- Weekly calculations -------------------------------------------
"""
def get_weekly_calculations(input_week, data):
    week_data = []

    if input_week == 1:
        week_data.extend(data[1:8])
    elif input_week == 2:
        week_data.extend(data[8:15])
    elif input_week == 3:
        week_data.extend(data[15:23])
    elif input_week == 4:
        week_data.extend(data[23:31])
    else:
        print()
        print(f"Incorrect selection. Try again.\n")

    if week_data:
        total_sales = sum(float(row[1]) for row in week_data)
        max_sales_day = max(week_data, key=lambda x: float(x[1]))
        min_sales_day = min(week_data, key=lambda x: float(x[1]))
        total_profit = sum(float(row[6]) for row in week_data)
        total_orders = sum(float(row[4]) for row in week_data)
        total_ad_budget = sum(float(row[5]) for row in week_data)
        average_check = total_sales / len(week_data)
        order_average_check = total_sales / total_orders
        conversion_rate = (total_orders / sum(float(row[2]) for row in week_data)) * 100
        roi = ((total_profit - total_ad_budget) / total_ad_budget) * 100

        print(f"\033[1mTotal sales for the {input_week} week: {total_sales}$\033[0m")
        print(f"\033[1mMaximum sales day for the {input_week} week: {max_sales_day[0]}, Sales: {max_sales_day[1]}$\033[0m")
        print(f"\033[1mMinimum sales day for the {input_week} week: {min_sales_day[0]}, Sales: {min_sales_day[1]}$\033[0m")
        print(f"\033[1mTotal profit for the {input_week} week: {total_profit}$\033[0m")
        print(f"\033[1mOrder average check for the {input_week} week: {order_average_check:.2f}$\033[0m")
        print(f"\033[1mConversion rate for the {input_week} week: {conversion_rate:.2f}%\033[0m")
        print(f"\033[1mTotal ad budget for the {input_week} week: {total_ad_budget}$\033[0m")
        print(f"\033[1mAverage check for the {input_week} week: {average_check:.2f}$\033[0m")
        print(f"\033[1mROI (Return on Investment) for the {input_week} week: {roi:.2f}%\033[0m")
    else:
        print()
        print(f"\033[1mNo data available for week {input_week}\033[0m\n")

"""
------------------------------------------------ Daily data ------------------------------------------------
"""
def get_daily_data(input_day, data):
    day_data = []

    # Go through all the data rows and find the ones that correspond to the specified day
    for row in data:
        date = row[0]  
        day = int(date.split('/')[0]) 

        if day == input_day:
            day_data.extend(row)

    if day_data:
        print(f"\033[1mSales for the {input_day} day: {day_data[1]}$\033[0m")
        print(f"\033[1mNumber of customers for the {input_day} day: {day_data[2]}\033[0m")
        print(f"\033[1mCost of sales for the {input_day} day: {day_data[3]}$\033[0m")
        print(f"\033[1mOrders for the {input_day} day: {day_data[4]}\033[0m")
        print(f"\033[1mAd budget for the {input_day} day: {day_data[5]}$\033[0m")
        print(f"\033[1mProfit for the {input_day} day: {day_data[6]}$\033[0m")
        print(f"\033[1mOrder average check for the {input_day} day: {day_data[7]}$\033[0m")
        print(f"\033[1mConversion rate for the {input_day} day: {day_data[8]}%\033[0m")
        print(f"\033[1mROI (Return on Investment) for the {input_day} day: {day_data[9]}%\033[0m")
    else:
        print(f"No data available for the {input_day} day")        
        

def show_about():
    print("Future description")

def main():
    while True:
        print()
        print("Select an option:")
        print("1. Start calculations")
        print("2. About")
        print("3. End program")
        
        choice = input("Enter an option number: ")
        print()

        if validate_data(choice, 1, 3):
            choice = int(choice)
            if choice == 1:
                start_calculations()
            elif choice == 2:
                show_about()
            elif choice == 3:
                break
            else:
                print("Incorrect selection. Try again.\n")

main()