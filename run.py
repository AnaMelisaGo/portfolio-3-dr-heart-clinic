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
    print('Test keywords: FRV= first visit, CKU= check-up, ECH= echocardio')
    print('EKG= electrocardiogram, STT= stress test, HOL= holter')
    print('Example: John Doe,FRV\n')
    while True:
        u_input = input("Patient's data:\n")
        us_input = u_input.split(',')
        user_input = [x.upper() for x in us_input]
        if validate_data(user_input):
            print('Valid data!')
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
                'Should be 2 data value separated by comma, ex: Name,TEST'
            )
        if data_value[1] not in patient_test:
            raise ValueError(
                f'Use keywords: {patient_test}, and comma with no spaces'
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


def exit_app():
    """
    A function that prompts a message exiting app
    """
    print('Saving your work... please wait!')
    time.sleep(2)
    print('Exiting app...')
    time.sleep(1)
    print('Bye!')


def update_file():
    """
    Function that leads user according to choices:
    - to update file
    - to calculate data and close the worksheet to create a new one
    - to save and exit the application
    """
    print('Choose an option:')
    update = input('A-update file|B-tally & calc|C-exit app\n').upper()
    if update == 'A':
        add_new_data()
    elif update == 'B':
        tally_worksheet()
    elif update == 'C':
        exit_app()
    else:
        print('Choose A, B, or C only')
        time.sleep(2)
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
            print('You are back to update/calculate section\n')
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
        print('\nYou have to create a new worksheet')
        print('Recommendation: use current "month-year" in naming file.\n')
        create_new_worksheet()
    else:
        print('Found the last file...')
        title = file_name()
        print(f'file name: {title} \n')
        time.sleep(1)


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
    # geek for geeks
    result = dict(zip(patient_test, total_test))
    print(f'\nThe result is:\n{result}\n')
    time.sleep(2)
    return total_test


def file_name():
    """
    Return file name of the last worksheet
    """
    last_ws = get_last_worksheet()
    title = last_ws.title
    return title


def row_data(file, tests):
    """
    Sum all test and convert all data into a single list
    """
    total = [sum(tests)]
    row = [[file], tests, total]
    # This pointer tutorial - convert list of list into flat list
    add_row = [item for elem in row for item in elem]
    return add_row


def update_total_tests(list_value):
    """
    Get the stadistic worksheet and add the values to the worksheet
    """
    total_test = CLINIC_SHEET.worksheet('total-tests')
    total_test.append_row(list_value)
    print('Updated total tests worksheet!\n')
    time.sleep(1)


def get_revenue(data):
    """
    To calculate revenue of each patient test and total
    """
    print('Calculating revenue...')
    time.sleep(1)
    price = CLINIC_SHEET.worksheet('dr-heart-revenue').row_values(4)[1:]
    tests = data[1:]
    revenue_list = []
    for num1, num2 in zip(price, tests):
        revenue_list.append(int(num1) * int(num2))
    return revenue_list


def add_data_revenue(file, rev):
    """
    To add the calculated revenue to the Dr Heart worksheet
    """
    rev_worksheet = CLINIC_SHEET.worksheet('dr-heart-revenue')
    rev_row = [[file], rev]
    add_rev_row = [cell for data in rev_row for cell in data]
    rev_worksheet.append_row(add_rev_row)
    print('Revenue worksheet updated!')
    time.sleep(1)
    keys = rev_worksheet.row_values(3)[1:]
    prices = [str(i)+'€' for i in rev]
    rev_result = dict(zip(keys, prices))
    print(f'\nTotal revenue in {file}:')
    print(rev_result)


def calculate_total_revenue():
    """
    To calculate and update the dr heart worksheets
    """
    test_list = get_test_column()
    w_name = file_name()
    data_list = row_data(w_name, test_list)
    update_total_tests(data_list)
    rev_data = get_revenue(data_list)
    add_data_revenue(w_name, rev_data)


def continue_working():
    """
    Function to continue working or exit app
    """
    print('\nIf you want to continue, press A. If exit app, press B')
    work_choice = input('Please select option:\n').upper()
    if work_choice == 'A':
        main()
    elif work_choice == 'B':
        exit_app()
    else:
        print('Only A or B is allowed. Please try again!')
        time.sleep(1)
        continue_working()


# Based on Derek Shidler Tutorial
def tally_worksheet():
    """
    To close worksheet and prepare it for calculation
    """
    last_worksheet = get_last_worksheet()
    print('You are about to tally and calculate current worksheet...')
    time.sleep(1)
    print("Remember once the worksheet is calculated, it won't be")
    print('accessible, and a new worksheet SHOULD be created.')
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
        print('Preparing worksheet...')
        # From Derek Shidler Tutorial
        time.sleep(1)
        calculate_total_revenue()
        continue_working()
    elif tally_input == 'N':
        print('You still can update')
        time.sleep(1)
        update_file()
    else:
        print('Invalid choice. Type Y or N only\n')
        time.sleep(1)
        tally_worksheet()


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


# DONE-change close function to tally function, put reminder once tallied
# DONE-file wont be accessible for update
# DONE-deploy to HEROKU
# DONE-need function to calculate tests
# DONE - another function to calculate total tests revenues
# DONE - add revenue to worksheet
# DONE - print latest data
# DONE - finished? add new function to choose whether add new ws or exit
# add try exception when creating new files with names that already exists
# exception APIError
