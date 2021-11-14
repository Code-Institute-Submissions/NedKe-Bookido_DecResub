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
                title = input('Enter product title:\n')
                description = input('Enter product description:\n')
                address = input('Enter product address:\n')
                capacity = input('Enter product capaity:\n')
                duration = input(
                    '\nEnter product duration in minutes ("e" for welcome screen):\n')
                price = input('Enter product price [0.2]:\n')
                date = input('Enter product date [2021-11-11]:\n')
                time = input('Enter product time [13:00:00]:\n')
                add_product_raw(title, description, address, price, capacity, duration, date, time)
                print('Product saved')
            return False
        print('You need to press "a" or "b"')


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


welcome_screen()