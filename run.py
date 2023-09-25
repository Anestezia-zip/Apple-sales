import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import warnings
from gspread import Worksheet
warnings.filterwarnings("ignore", category=UserWarning, module="gspread")

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
    print(f"A day with minimum sales {min_sales_day[0]}, sales: {min_sales_day[1]}$\n")

def update_worksheet_column(insert_column):
    """
    Updating a worksheet by adding a new column of data (insert_column) to the existing data. 
    It calculates the maximum number of columns, determines the number of rows in the insert_column, 
    and appends the data from insert_column to the last column of the existing data.
    """
    max_cols = max(len(row) for row in all_data)
    num_rows = len(insert_column)

    # Add the data array to the last column
    for i in range(num_rows):
        if i < len(all_data):
            all_data[i].append(str(insert_column[i]))
        else:
            # If there are more rows in insert_column than in the existing data, 
            # add empty cells for the missing rows in the existing data
            all_data.append([''] * (max_cols - 1) + [str(insert_column[i])])

    # Updating the data in the sheet
    sales.update('A1', all_data)
    print(f"Worksheet updated successfully with {insert_column[0]} column\n")

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
        # elif name == 'roi':
        #     profit = int(row[6])
        #     value = round((profit - ad_budget) / ad_budget, 2)
        #     label = 'ROI (Return on Investment)'
        elif name == 'average_check':
            value = round(daily_sales / orders, 2)
            label = 'Average check'
        elif name == 'conversion_rate':
            value = round(orders / customers, 2)
            label = 'Conversion rate'

        data_array.append(value)
    data_array.insert(0, label)    
    
    return data_array




def main():
    """ Run all program functions """
    get_weekly_sales()
    """  
    Call the calculate_data function with the required argument for each calculation and updating data in the table
    """
    profit_data = calculate_data('profit')
    update_worksheet_column(profit_data)
    average_check_data = calculate_data('average_check')
    update_worksheet_column(average_check_data)
    conversion_rate_data = calculate_data('conversion_rate')
    update_worksheet_column(conversion_rate_data)
main()