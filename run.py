import gspread
from google.oauth2.service_account import Credentials

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
    Get month sales figures input from the user. 

    """
    print("Please enter total sold units from last month following product order (Polo S/Polo M/Polo L/T-Shirt S/T-shirt M/T-shirt L/Jacket S/Jacket M/Jacket L).")
    print("Data should be nine numbers, separated by commas.")
    print("Examples: 10,5,40,50,100,88,2,15,120\n")

    data_str = input("Enter data here:\n")
    
    sales_data = data_str.split(",")
    validate_data(sales_data)


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 9 values.
    """
    try:
        if len(values) != 9:
            raise ValueError(
                f"Exactly 9 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
            


get_sales_data()

