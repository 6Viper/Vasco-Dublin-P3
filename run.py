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
    print(f"The data provided is {data_str}")


get_sales_data()

