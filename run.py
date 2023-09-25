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

def create_weekly_report():
    updated_data = sales.get_all_values()

    # Create a DataFrame from a list of data
    df = pd.DataFrame(updated_data[1:], columns=updated_data[0])

    # Create a PDF document
    doc = SimpleDocTemplate("weekly_report.pdf", pagesize=landscape(letter))

    # Collecting elements to add to the document
    elements = []

    # Add text in front of the table
    elements.append(Paragraph("Total sales", getSampleStyleSheet()['Heading1']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total sales for the week: {20800}$", getSampleStyleSheet()['Normal']))

    elements.append(Paragraph("Average check", getSampleStyleSheet()['Heading1']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"The average check: {round(20800 / 7)}$", getSampleStyleSheet()['Normal']))

    elements.append(Paragraph("Maximum and minimum sales:", getSampleStyleSheet()['Heading1']))
    elements.append(Spacer(1, 12))
    max_sales_day = max(data,  key=lambda x: int(x[1]))
    min_sales_day = min(data,  key=lambda x: int(x[1]))
    elements.append(Paragraph(f"A day with maximum sales {max_sales_day[0]}, sales: {max_sales_day[1]}$", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph(f"A day with minimum sales {min_sales_day[0]}, sales: {min_sales_day[1]}$", getSampleStyleSheet()['Normal']))
    elements.append(Spacer(1, 12))

    # Convert DataFrame to a ReportLab table
    # table_data = [list(df.columns)] + df.values.tolist()
    table_data = Table([df.columns.tolist()] + df.values.tolist())
    # table = Table(table_data)
    
    # Set table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    table_data.setStyle(style)

    # Add a table to the elements of a PDF document
    elements.append(table_data)

    # Ask the user if he/she wants to download the PDF
    download_choice = input("Would you like to download the report in PDF? (yes/no): ").lower()

    if download_choice == "yes":
        doc.build(elements)
        print("Report created and saved to file 'weekly_report.pdf'.")
    else:
        print("The report has not been downloaded.")

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
    roi_data = calculate_roi()
    update_worksheet_column(roi_data)
    
    create_weekly_report()
main()