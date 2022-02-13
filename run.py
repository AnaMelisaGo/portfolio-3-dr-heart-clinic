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
CLOSED_STYLE = {
        'textFormat': {
            'bold': True
        },
        'backgroundColor': {
            'red': 1,
            'green': 0.0,
            'blue': 0.0
        }
    }


# From Love Sandwich
def get_data():
    """
    Function to get the data from the application user
    """
    recom_msg = """
    PLEASE TYPE: Name,test_keyword (separated with comma, no spaces)
    Names can have spaces.
    Test keywords: FRV= first visit, CKU= check-up, ECH= echocardio
    EKG= electrocardiogram, STT= stress test, HOL= holter

    Example: John Doe,FRV\n
    """
    print(recom_msg)
    while True:
        u_input = input("Enter patient's data:\n")
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
        test_keyword = ['FRV', 'CKU', 'ECH', 'EKG', 'STT', 'HOL']
        if len(data_value) != 2:
            raise ValueError(
                'Should be 2 data value separated by comma, ex: Name,TEST'
            )
        if data_value[1] not in test_keyword:
            raise ValueError(
                f'Use keywords: {test_keyword}, and comma with no spaces'
            )
    except ValueError as error:
        print(f'Invalid data: {error}')
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


# Own code
def exit_app():
    """
    A function that prompts a message exiting app
    """
    print('\nSaving your work... please wait!')
    time.sleep(2)
    print('Exiting app...')
    time.sleep(1)
    print('Bye!')


# Based on Derek Shidler Tutorial for Adventure game
def add_new_data():
    """
    Function to get data and update file
    """
    print('\nUPDATE FILE')
    data = get_data()
    patient_data = list(data)
    update_last_worksheet(patient_data)


# Based on Love Sandwich with the help of GSPREAD DOC
def create_new_worksheet():
    """
    To create a new worksheet
    """
    while True:
        title = input('Type name for the new worksheet:\n')
        if validate_new_worksheet(title):
            print('Valid name!\n')
            break
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
    time.sleep(1)


# Own code
def show_all_sheet():
    """
    To show all worksheet title
    """
    all_worksheets = CLINIC_SHEET.worksheets()
    list_all_wsheet = []
    for index in range(len(all_worksheets)):
        list_all_wsheet.append(all_worksheets[index].title)
    return list_all_wsheet


# Based on Love Sandwich
def validate_new_worksheet(name):
    """
    To validate new workwheet
    """
    try:
        all_worksheet = show_all_sheet()
        if name in all_worksheet:
            raise ValueError(
                'Oops! Use another title for the worksheet!\n'
            )
    except ValueError as error:
        print(f'Invalid name: {error}')
        time.sleep(1)
        return False
    return True


# Own code mostly
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
    test_keyword = ['FRV', 'CKU', 'ECH', 'EKG', 'STT', 'HOL']
    total_test = [list_tests.count(test) for test in test_keyword]
    # geek for geeks
    result = dict(zip(test_keyword, total_test))
    print('\nThe overall result is:')
    for key, value in result.items():
        print(f'{key} = {value}')
        time.sleep(0.1)
    time.sleep(2)
    return total_test


# Own code with the help of GSPREAD DOC
def last_file_name():
    """
    Return file name of the last worksheet
    """
    last_ws = get_last_worksheet()
    title = last_ws.title
    return title


# Own code mostly
def row_data(file, tests):
    """
    Sum all test and convert all data into a single list
    """
    total = [sum(tests)]
    row = [[file], tests, total]
    # This pointer tutorial - convert list of list into flat list
    add_row = [item for elem in row for item in elem]
    return add_row


# Based on Love Sandwich
def update_total_tests(list_value):
    """
    Get the stadistic worksheet and add the values to the worksheet
    """
    total_test = CLINIC_SHEET.worksheet('total-tests')
    total_test.append_row(list_value)
    print('Updated Tests Stadistics worksheet!\n')
    time.sleep(1)


# Based on Love Sandwich
def get_revenue(data):
    """
    To calculate revenue of each patient test and total
    """
    print('Calculating revenue...')
    time.sleep(2)
    prices = CLINIC_SHEET.worksheet('dr-heart-revenue').row_values(4)[1:7]
    tests = data[1:7]
    test_rev = []
    for price, test in zip(prices, tests):
        test_rev.append(int(price) * int(test))
    total = [sum(test_rev)]
    rev = [test_rev, total]
    revenue_list = [x for y in rev for x in y]
    return revenue_list


# Based on Love Sandwich
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
    print(f'\nRevenue Report in {file}:')
    time.sleep(1)
    # Geeks for geeks string alignment
    print(f'{"TEST":<12}{"REVENUE":>5}')
    for key, val in rev_result.items():
        # Geeks for geeks string alignment
        print(f'{key:<12}{val:>5}')
        time.sleep(0.1)
    time.sleep(2)


# Own code
def calculate_total_revenue():
    """
    To calculate and update the dr heart worksheets
    """
    test_list = get_test_column()
    w_name = last_file_name()
    data_list = row_data(w_name, test_list)
    update_total_tests(data_list)
    rev_data = get_revenue(data_list)
    add_data_revenue(w_name, rev_data)


# Based on Derek Shidler Tutorial for Adventure game
def tally_worksheet():
    """
    To close worksheet and prepare it for calculation
    """
    last_worksheet = get_last_worksheet()
    tally_msg = """
TALLY AND CALCULATE WORKSHEETS
You are about to tally and calculate current worksheet...
    """
    print(tally_msg)
    time.sleep(1)
    reminder = """
    Remember this WON'T BE accessible for new data update.
    Once tallied, a new worksheet SHOULD be created.
    """
    print(reminder)
    time.sleep(3)
    last_worksheet.append_row(['CLOSED'])
    # from pretty printed Tutorials
    close_cell = last_worksheet.find('CLOSED').row
    last_worksheet.format(f'{close_cell}', CLOSED_STYLE)
    print('Preparing worksheet...')
    # From Derek Shidler Tutorial
    time.sleep(1)
    print('Fetching data... please wait!')
    time.sleep(1)
    calculate_total_revenue()


# Own code
def show_patients_file():
    """
    Show list of patients and tests worksheet
    """
    print('\nGetting files...')
    list_worksheets = show_all_sheet()
    patients_file = list_worksheets[2:]
    for p_lists in patients_file:
        print(p_lists)
        time.sleep(0.1)
    while True:
        p_lists_inp = input('\nSelect file:\n')
        if p_lists_inp in patients_file:
            show = CLINIC_SHEET.worksheet(p_lists_inp).get_all_values()
            for row in show:
                # Stackoverflow string formatting
                print(('{:<20}'*len(row)).format(*row))
                time.sleep(0.1)
            break
        if p_lists_inp not in patients_file:
            print('\nFile name does not exist!\n')
            time.sleep(1)


# Own code
def show_test_stats():
    """
    To show tests stadistics
    """
    test_stadistics = CLINIC_SHEET.worksheet('total-tests')
    tests_row = test_stadistics.get_all_values()
    print(f'{"TOTAL TESTS STATISTICS":^77}')
    for row in tests_row[2:]:
        # Stackoverflow string formatting
        print(('{:^10}'*len(row)).format(*row))
        time.sleep(0.2)


# Own code
def show_clinic_revenue():
    """
    To show the clinic revenue
    """
    clinic_rev_ws = CLINIC_SHEET.worksheet('dr-heart-revenue')
    clinic_rev = clinic_rev_ws.get_all_values()
    keys = clinic_rev[2]
    # Stackoverflow string formatting
    print(f'{"TOTAL CLINIC REVENUE":^77}')
    print(('{:^10}'*len(keys)).format(*keys))
    for row_rev in clinic_rev[4:]:
        cur = '€'
        file_name = row_rev[0]
        price = [str(i)+cur for i in row_rev[1:]]
        print(('{:^10}'*len(row_rev)).format(file_name, *price))
        time.sleep(0.2)


# Based on Derek Shidler Tutorial for Adventure game
def show_files():
    """
    To show data in a worksheet
    """
    while True:
        view_files = """\nVIEW FILES
Select an option:
A-View patients| B-Test Statistics| C-Revenue file| D-Back"""
        print(view_files)
        show_inp = input('\n').upper()
        if show_inp == 'A':
            show_patients_file()
            time.sleep(1)
        elif show_inp == 'B':
            show_test_stats()
            time.sleep(1)
        elif show_inp == 'C':
            show_clinic_revenue()
            time.sleep(1)
        elif show_inp == 'D':
            print('\nYou are back to MAIN MENU\n')
            time.sleep(2)
            break
        else:
            print('Invalid option. Please type A, B, or C only')
            time.sleep(2)


# Own code
def check_last_worksheet():
    """
    Check if last worksheet is closed and calculated
    """
    print('Checking files...')
    time.sleep(1)
    last_worksheet = get_last_worksheet()
    check_wksheet = last_worksheet.find('CLOSED')
    if check_wksheet:
        print('\nYou have to create a new worksheet')
        print('Recommendation: use current "month-year" in naming file.\n')
        create_new_worksheet()
    else:
        print('Found the last file...')
        time.sleep(1)
        title = last_file_name()
        print(f'FILE NAME: {title} \n')
        time.sleep(1)


def continue_working():
    """
    To continue
    """
    while True:
        cont_work = input('Continue working? Y / N\n').upper()
        if validate_cont_answer(cont_work):
            print('Ok!')
            break
    return cont_work


def validate_cont_answer(answer):
    """
    To validate continue answer
    """
    try:
        if answer not in ('Y' 'N'):
            raise ValueError(
                'Please enter Y or N only'
            )
    except ValueError as error:
        print(f'Invalid answer: {error}')
        return False
    return True


# Based on Derek Shidler Tutorial for Adventure game
def clinic_work():
    """
    Function that leads user according to choices:
    - to update file
    - to calculate data and close the worksheet to create a new one
    - to view different worksheets
    - to save and exit the application
    """
    while True:
        main_menu = """\nMAIN MENU
Choose an option:"""
        print(main_menu)
        work = input('A-Update file |B-Tally |C-View Files |D-Exit\n').upper()
        if work == 'A':
            add_new_data()
        elif work == 'B':
            tally_worksheet()
            cont_working = continue_working()
            if cont_working == 'Y':
                check_last_worksheet()
            if cont_working == 'N':
                exit_app()
                break
        elif work == 'C':
            show_files()
        elif work == 'D':
            exit_app()
            break
        else:
            print('Choose A, B, or C only')
            time.sleep(2)


# From Love Sandwich
def main():
    """
    Main function
    """
    check_last_worksheet()
    clinic_work()


if __name__ == "__main__":
    WELCOME_MSG = """
-----------------------------------------------------------------------
|                                                                     |
|                      Welcome to Dr. Heart Clinic                    |
|                                                                     |
-----------------------------------------------------------------------
"""
    print(WELCOME_MSG)
    main()
