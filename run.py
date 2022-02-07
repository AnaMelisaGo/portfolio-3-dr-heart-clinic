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
    print('\nPlease type: Name,test_keyword')
    print('Test keywords: FV= first visit, CKU= check-up, ECH= echocardio')
    print('EKG= electrocardiogram, STT= stress test, HOL= holter')
    print('Example: John Doe,FV\n')
    while True:
        u_input = input("Patient's data:\n")
        us_input = u_input.split(',')
        user_input = [x.upper() for x in us_input]
        if validate_data(user_input):
            print('Valid data!')
            time.sleep(1)
            break
    return user_input


# From Love Sandwich
def validate_data(value):
    """
    To validate input value
    """
    try:
        data_value = list(value)
        patient_test = ['FRV', 'CKU', 'ECH', 'EKG', 'STT', 'HOL']
        if len(data_value) != 2:
            raise ValueError(
                'Should be 2 data value separated by comma: Name,TEST'
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
    print('Worksheet updated!\n')
    time.sleep(1)


# Based on Derek Shidler Tutorial
def tally_worksheet():
    """
    To close worksheet and prepare it for calculation
    """
    last_worksheet = get_last_worksheet()
    print('You are about to tally and calculate current worksheet...')
    time.sleep(1)
    print("Remember once the worksheet is calculated, it won't be")
    print('accessible for new updates, and a new worksheet will be created.')
    time.sleep(2)
    tally_input = input('Tally worksheet? Y or N:\n').upper()
    if tally_input == 'Y':
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
    elif tally_input == 'N':
        print('You still can update')
        time.sleep(1)
        update_file()
    else:
        print('Invalid choice. Type Y or N only\n')
        time.sleep(1)
        tally_worksheet()


def update_file():
    """
    Function that leads user according to choices:
    - to update file
    - to calculate data and close the worksheet to create a new one
    - to save and exit the application
    """
    print('Choose an option:')
    update = input('A-update file|B-tally & calc wsheet|C-exit app\n').upper()
    if update == 'A':
        add_new_data()
    elif update == 'B':
        tally_worksheet()
    elif update == 'C':
        print('Saving your work... please wait!')
        time.sleep(2)
        print('Exiting app...')
        time.sleep(1)
        print('Bye!')
    else:
        print('Choose A, B, or C only')
        update_file()


def add_new_data():
    """
    Function to get data and update file
    """
    print('Please choose the following options:')
    while True:
        name = input('A -add new data| B -go back\n').upper()
        if name == 'A':
            data = get_data()
            patient_data = list(data)
            update_last_worksheet(patient_data)
        elif name == 'B':
            print('Back to update file or calculate worksheet\n')
            time.sleep(2)
            update_file()
            break
        else:
            print('Choose A or B only.')
            time.sleep(1)


def create_new_worksheet():
    """
    To create a new worksheet
    """
    title = input('Type file name for the new worksheet:\n')
    print('Creating new worksheet, please wait ...\n')
    time.sleep(2)
    new_worksheet = CLINIC_SHEET.add_worksheet(title, rows=100, cols=3)
    new_worksheet.update('A1:B1', [['NAME', 'TEST']])
    new_worksheet.format('A1:B1', {
        'textFormat': {
            'bold': True
        }
    })
    print('New worksheet is created!\n')


def check_last_worksheet():
    """
    Check if last worksheet is closed and calculated
    """
    last_worksheet = get_last_worksheet()
    check_wksheet = last_worksheet.find('CLOSED')
    if check_wksheet:
        print('You have to create a new worksheet')
        create_new_worksheet()
    else:
        print('Found the last file... \n')


def get_test_column():
    """
    Find all tests from the test column and count total data
    """
    last_ws = get_last_worksheet()
    find_test = last_ws.find('TEST')
    row_test = find_test.row
    col_test = find_test.col
    column = last_ws.col_values(col_test)
    list_tests = column[row_test:]
    patient_test = ['FRV', 'CKU', 'ECH', 'EKG', 'STT', 'HOL']
    total_test = [list_tests.count(test) for test in patient_test]
    print(total_test)
    return total_test


def sum_up(tests):
    """
    dadfaf
    """
    last_ws = get_last_worksheet()
    file_name = [last_ws.title]
    total = [sum(tests)]
    row = [file_name, tests, total]
    # This pointer tutorial - convert list of list into flat list
    add_row = [item for elem in row for item in elem]
    return add_row


def update_total_tests(list_value):
    """
    Get total of test
    """
    total_test = CLINIC_SHEET.worksheet('total-tests')
    total_test.append_row(list_value)
    print('updated total tests worksheet')


def main():
    """
    Main function
    """
    check_last_worksheet()
    update_file()


print('-'*60)
print('      Welcome to Dr. Heart Clinic')
print('-'*60)
# main()
test_list = get_test_column()
data_list = sum_up(test_list)
update_total_tests(data_list)


# DONE-change close function to tally function, put reminder once tallied
# DONE-file wont be accessible for update
# DONE-deploy to HEROKU
# need function to calculate tests
# another function to calculate total tests revenues
# print latest data
# when all finished, add new function to choose whether add new wksheet or exit