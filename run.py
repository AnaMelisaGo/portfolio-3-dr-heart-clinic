import time
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
CLINIC_SHEET = GSPREAD_CLIENT.open('dr-heart-clinic')


# From Love Sandwich
def get_data():
    """
    Function to get the data from the application user
    """
    u_input = input("Please type the patient's: Name, Test:\n")
    user_input = u_input.split(',')
    validate_data(user_input)
    return user_input


# From Love Sandwich
def validate_data(value):
    """
    To validate input value
    """
    try:
        data_value = list(value)
        if data_value != 2:
            raise ValueError(
                'Should be 2 data value: Name, Test'
            )
    except ValueError as e:
        print(f'Invalid data: {e}')


# Own code
def get_last_worksheet():
    """
    To get the last worksheet
    """
    worksheet = CLINIC_SHEET.get_worksheet(-1)
    return worksheet


# From Love Sandwich
def update_last_worksheet(data):
    """
    To add new data to the last worksheet
    """
    last_worksheet = get_last_worksheet()
    last_worksheet.append_row(data)
    print('Worksheet updated\n')


# Based on Derek Shidler Tutorial
def close_worksheet():
    """
    To close worksheet and prepare it for calculation
    """
    last_worksheet = get_last_worksheet()
    close_input = input('Close worksheet? Y or N:\n').upper()
    if close_input == 'Y':
        last_worksheet.append_row(['CLOSED'])
        # from pretty printed Tutorials
        close_cell = last_worksheet.find('CLOSED').row
        last_worksheet.format(f'A{close_cell}', {
            'textFormat': {
                'bold': True
            },
            'backgroundColor': {
                'red': 1,
                'green': 0.0,
                'blue': 0.0
            }
        })
        print('Worksheet closed')
        # From Derek Shidler Tutorial
        time.sleep(1)
    elif close_input == 'N':
        print('You still can update')
        time.sleep(1)
    else:
        print('Invalid choice. Type Y or N only\n')
        time.sleep(1)
        close_worksheet()


def check_last_worksheet():
    """
    Check if last worksheet is closed and calculated
    """
    last_worksheet = get_last_worksheet()
    check_wksheet = last_worksheet.find('CLOSED')
    if check_wksheet:
        print('You have to create a new worksheet')
        title = input('Type file name for the new worksheet:\n')
        print('Creating new worksheet, please wait ...\n')
        new_worksheet = CLINIC_SHEET.add_worksheet(title, rows=100, cols=3)
        new_worksheet.update('A1:B1', [['NAME', 'TEST']])
        new_worksheet.format('A1:B1', {
            'textFormat': {
                'bold': True
            }
        })
        print('New worksheet is created!\n')
    else:
        print('Can update')


def main():
    """
    Main function
    """
    patient_data = get_data()
    update_last_worksheet(patient_data)


print('-'*60)
print('      Welcome to Dr. Heart Clinic')
print('-'*60)
# main()
close_worksheet()
