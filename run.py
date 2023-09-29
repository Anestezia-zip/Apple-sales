import gspread
from google.oauth2.service_account import Credentials
from tabulate import tabulate
from pyfiglet import figlet_format
import sys

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
all_data = sales.get_all_values()
data = all_data[1:]


def validate_data(input_value, min_value, max_value):
    """
    Validates user input and make sure that it is within the given range.
    """
    try:
        value = int(input_value)
        if min_value <= value <= max_value:
            return True

        print(
            f"\033[1m Input must be a number between {min_value}"
            f" and {max_value}.\033[0m\n"
        )
    except ValueError:
        print("\033[1m Input must be a number.\033[0m\n")

    return False


def get_total_sales():
    print('\033[1m Getting sales...\033[0m\n')
    total_sales = sum(int(row[1]) for row in data)
    print(f"\033[1m Total sales: {total_sales}$\033[0m\n")

    return total_sales


def get_average_check(total_sales, days):
    print('\033[1m Getting average check...\033[0m\n')
    average_check = round(total_sales / days)
    print(f"\033[1m The average check: {round(average_check)}$\033[0m\n")

    return average_check


def get_maximum_sales():
    max_sales_day = max(data,  key=lambda x: int(x[1]))
    print(
        f"\033[1m A day with maximum sales {max_sales_day[0]}, "
        f"sales: {max_sales_day[1]}$\033[0m\n"
    )

    return max_sales_day


def get_minimum_sales():
    min_sales_day = min(data, key=lambda x: int(x[1]))
    print(
        f"\033[1m A day with minimum sales {min_sales_day[0]},"
        f" sales: {min_sales_day[1]}$\033[0m\n"
    )

    return min_sales_day


def calculate_mounthly_data(name):
    """
    Calculate and display monthly data based on the specified metric.

    This function takes a metric name as input ('Profit', 'Сonversion rate',
    or 'Conversion rate'),
    processes the data for each day, and returns a list of monthly values
    rounded to two decimal places.
    """
    data_array = []

    for row in data:
        date = row[0]
        daily_sales, customers, cost, orders, ad_budget, profit = [
            float(x) for x in row[1:7]
        ]

        if name == 'Profit':
            value = daily_sales - cost
            label = '$'
        elif name == 'Order average check':
            value = round(daily_sales / orders, 2)
            label = '$'
        elif name == 'Conversion rate':
            value = orders / customers * 100
            label = '%'
        elif name == 'ROI (Return on Investment)':
            value = (profit - ad_budget) / ad_budget * 100
            label = '%'

        data_array.append([date, round(value, 2)])
    print(f'\033[1m Getting {name} for the month...\033[0m\n')
    print(
        tabulate(
            data_array,
            headers=["Date", f"{name} ({label})"],
            tablefmt="pretty"
        )
    )
    print()
    return data_array


def start_calculations():
    """
    Display a menu of options for various calculations and perform the selected
    action.

    The user can choose an option by entering the corresponding number.
    The function then validates the input, performs the selected action, and
    continues to loop until the user chooses to go back to the main menu
    or end the program.
    """
    while True:
        print("Select an option:")
        print("1. Get monthly calculations")
        print("2. Get weekly calculations")
        print("3. Get daily data")
        print("4. Back to the main menu")
        print("5. End program")

        choice = input("Enter the option number: ")
        print()

        if validate_data(choice, 1, 5):
            choice = int(choice)
            if choice == 1:
                get_monthly_calculations()
            elif choice == 2:
                input_week = input("Enter the week number (1, 2, 3, or 4): ")
                if validate_data(input_week, 1, 4):
                    input_week = int(input_week)
                    get_weekly_calculations(input_week)
            elif choice == 3:
                input_day = input(
                    "Enter the date (in the format DD: 1 to 30): "
                )
                if validate_data(input_day, 1, 30):
                    input_day = int(input_day)
                    get_daily_data(input_day)
            elif choice == 4:
                break
            elif choice == 5:
                sys.exit()


def get_monthly_calculations():
    """
    Display a menu of options for monthly calculations and perform the selected
    action.

    The user can choose an option by entering the corresponding number.
    The function then validates the input,
    performs the selected action, and continues to loop until the user chooses
    to go back to the previous menu or end the program.
    """
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

        choice = input("Enter the option number: ")
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
                calculate_mounthly_data('Conversion rate')
            elif choice == 9:
                calculate_mounthly_data('ROI (Return on Investment)')
            elif choice == 10:
                break
            elif choice == 11:
                sys.exit()


def get_full_monthly_report():
    """
    Generate and display a full monthly report with various data metrics.
    The function retrieves the necessary data and metrics from other functions
    and displays them in a formatted table.
    """
    total_sales = get_total_sales()
    get_average_check(total_sales, 30)
    get_maximum_sales()
    get_minimum_sales()
    table = tabulate(data, headers=all_data[0], tablefmt="simple")
    print(table)


def get_weekly_calculations(input_week):
    """
    Calculate and display weekly data metrics for the specified week.

    :param input_week: The week number to calculate metrics for (1, 2, 3, or 4)
    :type input_week: int
    :param data: The dataset containing daily sales and other relevant data.
    :type data: list of lists
    :return: None
    """

    week_data = []

    if input_week == 1:
        week_data = data[0:7]
        print(week_data)
    elif input_week == 2:
        week_data = data[7:14]
    elif input_week == 3:
        week_data = data[14:22]
    elif input_week == 4:
        week_data = data[22:30]

    if week_data:
        total_sales = sum(float(row[1]) for row in week_data)
        max_sales_day = max(week_data, key=lambda x: float(x[1]))
        min_sales_day = min(week_data, key=lambda x: float(x[1]))
        total_profit = sum(float(row[6]) for row in week_data)
        total_orders = sum(float(row[4]) for row in week_data)
        total_ad_budget = sum(float(row[5]) for row in week_data)
        average_check = total_sales / len(week_data)
        order_average_check = total_sales / total_orders
        conversion_rate = (
                total_orders / sum(float(row[2]) for row in week_data)) * 100
        roi = ((total_profit - total_ad_budget) / total_ad_budget) * 100

        print(
            f"\033[1m Total sales for the {input_week} week: "
            f"{total_sales}$\033[0m"
        )
        print(
            f"\033[1m Maximum sales day for the {input_week} week: "
            f"{max_sales_day[0]}, Sales: {max_sales_day[1]}$\033[0m"
        )
        print(
            f"\033[1m Minimum sales day for the {input_week} week: "
            f"{min_sales_day[0]}, Sales: {min_sales_day[1]}$\033[0m"
        )
        print(
            f"\033[1m Total profit for the {input_week} week: "
            f"{total_profit}$\033[0m"
        )
        print(
            f"\033[1m Order average check for the {input_week} week: "
            f"{order_average_check:.2f}$\033[0m"
        )
        print(
            f"\033[1m Conversion rate for the {input_week} week: "
            f"{conversion_rate:.2f}%\033[0m"
        )
        print(
            f"\033[1m Total ad budget for the {input_week} week: "
            f"{total_ad_budget}$\033[0m"
        )
        print(
            f"\033[1m Average check for the {input_week} week: "
            f"{average_check:.2f}$\033[0m"
        )
        print(
            f"\033[1m ROI (Return on Investment) for the {input_week} week: "
            f"{roi:.2f}%\033[0m\n"
        )
    else:
        print(f"\n\033[1m No data available \033[0m\n")


def get_daily_data(input_day):
    """
    Retrieve and display daily data metrics for the specified day.

    :param input_day: The day of the month for which to retrieve data (1 to 30)
    :type input_day: int
    :param data: The dataset containing daily sales and other relevant data.
    :type data: list of lists
    :return: None
    """
    day_data = []

    for row in data:
        date = row[0]
        day = int(date.split('/')[0])

        if day == input_day:
            day_data = row

    if day_data:
        print(f"\033[1m Sales for the {input_day} day: {day_data[1]}$\033[0m")
        print(
            f"\033[1m Number of customers for the {input_day} day: "
            f"{day_data[2]}\033[0m"
        )
        print(
            f"\033[1m Cost of sales for the {input_day} day: "
            f"{day_data[3]}$\033[0m"
        )
        print(f"\033[1m Orders for the {input_day} day: {day_data[4]}\033[0m")
        print(
            f"\033[1m Ad budget for the {input_day} day: {day_data[5]}$\033[0m"
        )
        print(f"\033[1m Profit for the {input_day} day: {day_data[6]}$\033[0m")
        print(
            f"\033[1m Order average check for the {input_day} day: "
            f"{day_data[7]}$\033[0m"
        )
        print(
            f"\033[1m Conversion rate for the {input_day} day: "
            f"{day_data[8]}%\033[0m"
        )
        print(
            f"\033[1m ROI (Return on Investment) for the {input_day} day: "
            f"{day_data[9]}%\033[0m"
        )
    else:
        print(f"\033[1m No data available \033[0m")


def show_about():
    print(
        "\033[1m This program provides various options for performing "
        "calculations and obtaining data.\033[0m"
    )
    print(
        "\033[1m Users can choose between monthly, weekly, and daily "
        "calculations, and access a range of specific metrics related to "
        "sales and performance.\033[0m"
    )
    print(
        "\033[1m Overall, it seems like a versatile tool for analyzing and "
        "calculating various aspects of data and performance.\033[0m\n"
    )

    print("\033[1m 1. Get total sales:\033[0m")
    print(
        "   - Purpose: This calculation provides the total sales revenue for "
        "a specific period (e.g., month, week, or day). It gives you an "
        "overview of the overall revenue generated during that time frame.\n"
    )

    print("\033[1m 2. Get average check:\033[0m")
    print(
        "   - Purpose: The average check calculates the average amount of "
        "money spent per transaction in a given week or month. It helps in "
        "understanding customer spending patterns on a weekly/monthly basis.\n"
    )

    print("\033[1m 3. Get maximum sales:\033[0m")
    print(
        "   - Purpose: This calculation identifies the highest sales figure "
        "within the chosen period. It helps in recognizing the peak "
        "performance and the highest revenue achieved.\n"
    )

    print("\033[1m 4. Get minimum sales:\033[0m")
    print(
        "   - Purpose: Similar to maximum sales, this calculation identifies "
        "the lowest sales figure within the chosen period. It helps in "
        "identifying periods of low performance or potential issues.\n"
    )

    print("\033[1m 5. Get profit:\033[0m")
    print(
        "   - Purpose: Profit calculation subtracts the costs or expenses "
        "from the total revenue. It provides insights into the profitability "
        "of your business for a specific time frame.\n"
    )

    print("\033[1m 6. Get order average check:\033[0m")
    print(
        "   - Purpose: The order average check calculates the average amount "
        "spent by customers per order. It helps in understanding individual "
        "purchase behavior and can guide pricing strategies.\n"
    )

    print("\033[1m 7. Get conversion rate:\033[0m")
    print(
        "   - Purpose: Conversion rate measures the percentage of customers "
        "who take a desired action, such as making a purchase or completing a "
        "form. It helps evaluate the effectiveness of marketing campaigns and "
        "website optimization.\n"
    )

    print("\033[1m 8. Get ROI (Return on Investment):\033[0m")
    print(
        "   - Purpose: ROI measures the return (profit) on an investment "
        "relative to the initial cost (investment). It is used to assess the "
        "performance and profitability of investments or marketing campaigns. "
        "A positive ROI indicates profitability.\n"
    )


def main():
    print(figlet_format("apple sales reports", font="larry3d"))
    while True:
        print("\nSelect an option:")
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


if __name__ == "__main__":
    main()
