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
SHEET = GSPREAD_CLIENT.open('Vasco-Dublin')


def get_sales_data():
    """
    Get month sales figures input from the user. Run a while loop to collect a valid
    string of data from the user via the terminal, which must be a string of 9 numbers
    separated by commas. The loop will repeatedly request data until proofs valid. 

    """
    while True:
        print("Please enter total sold units from last month following product order (Polo S/Polo M/Polo L/T-Shirt S/T-shirt M/T-shirt L/Jacket S/Jacket M/Jacket L).")
        print("Data should be nine numbers, separated by commas.")
        print("Examples: 10,5,40,50,100,88,2,15,120\n")

        data_str = input("Enter data here:\n")
        
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data    


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 9 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 9:
            raise ValueError(
                f"Exactly 9 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
            
    return True


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """

    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates carryover stock and possible excess on warehouse.
    - Negative surplus indicates amount of items that required an extra order from 
    manufacturer with extra cost, and requires data to be analysed for future, as well
    as to assist next stock calculation.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def get_bimestrial_entries_sales():
    """
    " Collects data from sales worksheet, collecting only bimestrial period last year, 
    returning data as a list of lists to be used on stock data calculation".
    """
    sales = SHEET.worksheet("sales")
    
    columns = []
    for ind in range(1, 10):
        column = sales.col_values(ind)
        columns.append(column[-12:-10])

    return columns    


def calculate_stock_data(data):
    """
    Calculate the average sold from two months(same month plus following month) 
    last year times 15% marketing target.
    """  
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.15
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_bimestrial_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

    return stock_data

print("Welcome to Vasco Dublin Data Automation.\n")
stock_data = main()


def get_stock_values(data):
    """
    Print out the calculated stock numbers for next month.
    """
    headings = SHEET.worksheet('stock').row_values(1)
    print("Make a request to central depot for the next month:\n")

    new_data = {}
    for heading, stock_num in zip(headings, data):
        new_data[heading] = stock_num

    return new_data

stock_values = get_stock_values(stock_data)
print(stock_values)