"""
run module is the main entry point of the application
It provides a command line interface for admins to create new product and
customers to book a product
"""

import re
from datetime import datetime
import os
from dotenv import load_dotenv
from sheet import list_products, add_booking, add_product_raw, \
    CapacityReachedException, CustomerAlreadyRegistered
from utils import isValidEmail

load_dotenv()


def welcome_screen():
    """
    Welcomes the user and shows options to either book a product or as an admin
    to add a new product
    """
    print('Welcome to Bookido. Your hub to book amazing experiences ')
    print('such as Wine testing, Massage, Tourism activities and so on.\n\n')
    while True:
        chosen_option = input(
            '\nPress "b" to book a product or "a" for admin panel:\n\n')

        chosen_option = chosen_option.lower()

        if chosen_option == 'b':
            customer_flow()
            return False
        if chosen_option == 'a':
            attempts = 0
            while True:
                if attempts == 3:
                    print('\nToo many wrong passwords. '
                          'Try again at later time.!')
                    welcome_screen()
                    return False
                password = input('Please enter password:\n')
                if password == os.getenv('ADMIN_PASSWORD'):
                    add_product_prompt()
                    return False
                print('Wrong password, Try again\n')
                attempts = attempts + 1
        print('You need to press "a" or "b"')


def add_product_prompt():
    """
    Adds a product to the product catalog by asking the admin to add
    information about that product
    """
    print("\nAdding a new product. Please answer following questions:\n")
    title = get_validated_input('Product title')

    description = get_validated_input('Product description')

    address = get_validated_input('Product address')

    capacity = get_validated_integer_input('Product capacity')

    duration = get_validated_integer_input('Product duration', 'in minutes')

    price = get_validated_float_input('Product price')

    while True:
        date = input(
            f'\nEnter product date (example: '
            f'{datetime.now().strftime("%Y-%m-%d")}) '
            f'("e" for welcome screen):\n')
        exit_to_main_screen(date)
        if not re.match(r'\d{4}-\d{2}-\d{2}', date):
            print(
                f'Please enter date in the format as this example: '
                f'{datetime.now().strftime("%Y-%m-%d")}\n')
        elif datetime.now().date() > datetime.strptime(date, '%Y-%m-%d').date():
            print('Enter a date later or equal to today')
        else:
            break

    while True:
        time = input(
            f'\nEnter product time (example: '
            f'{datetime.now().strftime("%H:%M:%S")}) '
            f'("e" for welcome screen):\n')
        exit_to_main_screen(time)
        if not re.match(r'\d{2}:\d{2}:\d{2}', time):
            print('Please enter time in the format as '
                  'this example: 13:00:00\n')
        elif datetime.now() >= datetime.strptime(
           f'{date} {time}', '%Y-%m-%d %H:%M:%S'):
            print('Enter a time that is later than current time\n')
        else:
            break

    print(
        f'\nConfirm adding {title} on {date} at {time} with price {price} €:')
    confirm = input('(y): Yes, n: (No)\n')
    if confirm.lower() == 'y':
        print("Saving the product please wait ...")
        add_product_raw(
            title,
            description,
            address,
            price,
            capacity,
            duration,
            date,
            time)
        print('Product saved.')
        input('\nPress any key to go to welcome screen: \n')
        welcome_screen()
    if confirm.lower() == 'n':
        chosen_option = input('(1): Add new product, (e): main screen')
        exit_to_main_screen(chosen_option)
        if chosen_option == '1':
            add_product_prompt()


def get_validated_input(field_label):
    """
    Asks user for an input and validates that it's not empty
    :param field_label: The label for the input
    """
    while True:
        field = input(f'\nEnter {field_label} (Press "e" for welcome screen):'
                      f'\n')
        if field.strip() == '':
            print(f'{field_label} can not be empty!')
        else:
            return exit_to_main_screen(field)


def get_validated_integer_input(field_label, extra_info=None):
    """
    Asks user for an input and validates that it is a number bigger than 0
    :param field_label: The label for the input
    :param extra_info: Extra info to include in the prompt
    """
    extra = extra_info if extra_info else ''
    while True:
        field = input(
            f'\nEnter {field_label} {extra} (Press "e" for welcome screen):\n')
        try:
            numeric_field = int(field)
            if numeric_field <= 0:
                print(f'{field_label} should be a number bigger than 0')
            else:
                return exit_to_main_screen(field)
        except ValueError:
            print(f'{field_label} should be a number bigger than 0')

def get_validated_float_input(field_label):
    """
    Asks for user input and validates that it is a float number
    :param field_label: The label for the input
    """
    while True:
        field = input(f'\nEnter {field_label} (Press "e" for welcome screen):'
                      f'\n')
        try:
            numeric_field = float(field)
            if numeric_field <= 0:
                print(f'{field_label} should be a number bigger than 0')
            else:
                return exit_to_main_screen(field)
        except ValueError:
            print(f'{field_label} should be a number bigger than 0')


def customer_flow():
    """
    Goes through the process of booking a product for a customer by listing
    available products for the user to choose, shows chosen
    product's information such as description, address and price, and
    get a customer's email address to book and confirm the product.
    """
    print('\nFollowing is the list of products you can choose from:\n')
    products = list_products()
    formatted_products_to_choose = ''
    if len(products) == 0:
        input(
            'There no product available at this time. '
            'Press any key for main screen:\n')
        welcome_screen()
    for product_row in products:
        formatted_products_to_choose += \
            f'{product_row.product.id}: {product_row.product.title}\n'
    chosen_product = None
    while True:
        print(formatted_products_to_choose)
        chosen_product = input(
            '\nChoose the number in front of the product to book '
            '(e to show main screen):\n')
        exit_to_main_screen(chosen_product)
        if chosen_product == '':
            print('\nWrong entry. Enter the number in front of the product!\n')
        else:
            try:
                chosen_product = int(chosen_product)
                if int(chosen_product) not in\
                   list(map(lambda p: p.product.id, products)):
                    print('\nWrong entry. Enter the number in front of '
                          'the produc!t\n')
                else:
                    break
            except ValueError:
                print('\nWrong entry. Enter the number in front of'
                      ' the product\n')
    selected_product = list(
        filter(
            lambda p: p.product.id == chosen_product,
            products))[0].product

    print(
        f'\n{selected_product.title} is available on '
        f'{selected_product.date} at {selected_product.time}')
    print(f'Description: {selected_product.description}')
    print(f'Address: {selected_product.address}')
    print(f'Price: {selected_product.price} €')
    print(
        '\nUpon continuing, your information will be saved in '
        'our datastore.\n')
    chosen_option = input('(a): continue. (p): product menu, '
                          '(e): welcome screen\n')
    exit_to_main_screen(chosen_option)
    exit_to_product_menu(chosen_option)

    if chosen_option == 'a':
        customer_email = get_and_validate_email()
        print(
            f'\nConfirm booking of {selected_product.title} '
            f'on {selected_product.date} at {selected_product.time}?\n')
        yes_no = input(
            '(y): Yes, (n): No, (p): Product menu, (e): Welcome screen\n\n')
        exit_to_product_menu(yes_no)
        exit_to_main_screen(yes_no)

        if yes_no.lower() == 'y':
            print('Adding your booking, please wait ...')
            try:
                add_booking(chosen_product, customer_email)
            except CapacityReachedException:
                print(
                    '\nUnfortunately the capacity for this event is '
                    'reached.\n')
                chosen_input = input(
                    '(p): Try another product, (e): Welcome screen\n')
                exit_to_main_screen(chosen_input)
                exit_to_product_menu(chosen_input)
            except CustomerAlreadyRegistered:
                print('You are already booked for this product.')
                user_input = input('(p): Product menu, (e): Welcome screen\n')
                exit_to_product_menu(user_input)
                exit_to_main_screen(user_input)
            print(
                f'You are booked for {selected_product.title} '
                f'on {selected_product.date} at {selected_product.time}')
            input('\nPress any key to go to welcome screen:\n')
            welcome_screen()
        else:
            welcome_screen()


def exit_to_main_screen(user_input):
    """
    Helper function to go to the main screen
    :param user_input:
    """
    if user_input.lower() == 'e':
        welcome_screen()
    return user_input


def exit_to_product_menu(user_input):
    """
    Helper function to go to the product menu
    :param user_input:
    """
    if user_input.lower() == 'p':
        customer_flow()


def get_and_validate_email():
    """
    Asks for user input for an email, valiate if it's in the correct format and
    if not, it alerts that the format is wrong and asks the user again for an
    email
    """
    while True:
        customer_email = input('Enter your email address to book:\n')
        if not isValidEmail(customer_email):
            print('\nWrong email. Please try again!')
        else:
            return customer_email


welcome_screen()
