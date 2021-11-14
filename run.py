"""
run module is the main entry point of the application
It provides a command line interface for admins to create new product and
customers to book a product
"""

from sheet import list_products, add_booking, add_product_raw


def welcome_screen():
    """
    Welcomes the user and shows options to either book a product or as an admin
    to add a new product
    """
    while True:
        chosen_option = input(
            'Press "b" to book a product or "a" for admin panel:\n\n')

        chosen_option = chosen_option.lower()

        if chosen_option == 'b':
            customer_flow()
            return False
        if chosen_option == 'a':
            password = input('Please enter password:\n')
            if password == 'password':
                add_product_prompt()

            return False
        print('You need to press "a" or "b"')


def add_product_prompt():
    """
    Adds a product to the product catalog by asking the admin to add information
    about that product
    """
    print("Adding a new product. Please answer following questions:\n")
    title = input('Enter product title (Press "e" for welcome screen):\n')
    exit_to_main_screen(title)
    description = input(
        '\nEnter product description ("e" for welcome screen):\n')
    exit_to_main_screen(description)
    address = input('\nEnter product address ("e" for welcome screen):\n')
    exit_to_main_screen(address)
    capacity = input('\nEnter product capacity ("e" for welcome screen):\n')
    exit_to_main_screen(capacity)
    duration = input(
        '\nEnter product duration in minutes ("e" for welcome screen):\n')
    exit_to_main_screen(duration)
    price = input('\nEnter product price ("e" for welcome screen):\n')
    exit_to_main_screen(price)

    while True:
        date = input(
            f'Enter product date (example: '
            f'{datetime.now().strftime("%Y-%m-%d")}) '
            f'("e" for welcome screen):\n')
        exit_to_main_screen(date)
        if not re.match(r'\d{4}-\d{2}-\d{2}', date):
            print(
                f'Please enter date in the format as this example: '
                f'{datetime.now().strftime("%Y-%m-%d")}\n')
        if datetime.now().date() > datetime.strptime(date, '%Y-%m-%d').date():
            print('Enter a date later or equal to today')
        else:
            break

    while True:
        time = input(
            f'Enter product time (example: '
            f'{datetime.now().strftime("%H:%M:%S")}) '
            f'("e" for welcome screen):\n')
        exit_to_main_screen(time)
        if not re.match(r'\d{2}:\d{2}:\d{2}', date):
            print('Please enter time in the format as this example: 13:00:00\n')
        if datetime.now() >= datetime.strptime(
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


def customer_flow():
    print('Following is the list of products you can choose from:\n')
    products = list_products()
    formatted_products_to_choose = ''
    for product_row in products:
        formatted_products_to_choose += product_row.product.id + ': ' + product_row.product.title + '  '
    print(formatted_products_to_choose)
    chosen_product = input(
        'Choose the number in front of the product to book:\n')
    selected_product = list(filter(lambda p: p.product.id == chosen_product, products))[0].product

    print(
        f'{selected_product.title} is available on {selected_product.date} at {selected_product.time}')

    chosen_option = input(
        '(a): continue. (p): product menu, (b):welcome screen\n')
    if chosen_option == 'a':
        customer_email = input('Enter your email address to book:\n')
        # validate email
        add_booking(chosen_product, customer_email)
        print(
            f'You are booked for {selected_product.title} on {selected_product.date} at {selected_product.time}')
    if chosen_option == 'p':
        show_products()
    if chosen_option == 'b':
        splash()


def exit_to_main_screen(user_input):
    """
    Helper function to go to the main screen
    :param user_input:
    """
    if user_input.lower() == 'e':
        welcome_screen()


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