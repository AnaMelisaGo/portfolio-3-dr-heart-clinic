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
    print('Please type: Name,test_keyword')
    print('Test keywords: FV= first visit, CKU= check-up, ECH= echocardio')
    print('EKG= electrocardiogram, STT= stress test, HOL= holter\n')
    print('Example: John Doe,FV')
    while True:
        u_input = input("Patient's data:\n")
        us_input = u_input.split(',')
        user_input = [x.upper() for x in us_input]
        print(user_input)
        if validate_data(user_input):
            print('ok')
            break
    return user_input


# From Love Sandwich
def validate_data(value):
    """
    To validate input value
    """
    try:
        data_value = list(value)
        patient_test = ['FV', 'CKU', 'ECH', 'EKG', 'STT', 'HOL']
        if len(data_value) != 2:
            raise ValueError(
                'Should be 2 data value: Name, Test'
            )
        if data_value[1] not in patient_test:
            raise ValueError(
                f'Use test keywords: {patient_test}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}')
        return False
    return True


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
    print('You are about to close and calculate current worksheet...')
    time.sleep(2)
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


def update_file():
    """
    Function that leads user according to choices:
    - to update file
    - to calculate data and close the worksheet to create a new one
    - to save and exit the application
    """
    print('A -update file| B -close and calc worksheet| C -exit app')
    update_input = input('Choose an option: \n').upper()
    if update_input == 'A':
        add_new_data()
    elif update_input == 'B':
        close_worksheet()
    elif update_input == 'C':
        print('Saving your work...')
        time.sleep(2)
        print('Exiting app...')
        time.sleep(1)
        print('Bye!')
    else:
        print('Only A, B, or C is allowed')
        update_file()


def add_new_data():
    """
    Function to get data and update file
    """
    print('Please choose the following options:')
    name = input('A -add new data| B -go back\n').upper()
    if name == 'A':
        data = get_data()
        patient_data = list(data)
        update_last_worksheet(patient_data)
    if name == 'B':
        print(f'Opps your name is {name}')


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
        print('Found the last file... \n')


def main():
    """
    Main function
    """
    check_last_worksheet()
    update_file()


print('-'*60)
print('      Welcome to Dr. Heart Clinic')
print('-'*60)
main()
# add_new_data()
# get_data()
