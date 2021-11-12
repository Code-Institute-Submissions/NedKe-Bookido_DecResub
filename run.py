# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
from sheet import list_products, add_booking, add_product_raw


def splash():
    while True:
        chosen_option = input(
            'Press "b" to book a product or "a" for admin panel:\n\n')

        chosen_option = chosen_option.lower()

        if chosen_option == 'b':
            show_products()
            return False
        if chosen_option == 'a':
            password = input('Please enter password:\n')
            if password == 'password':
                title = input('Enter product title:\n')
                description = input('Enter product description:\n')
                address = input('Enter product address:\n')
                capacity = input('Enter product capaity:\n')
                price = input('Enter product price [0.2]:\n')
                date = input('Enter product date [2021-11-11]:\n')
                time = input('Enter product time [13:00:00]:\n')
                add_product_raw(title, description, address, price, capacity, date, time)
                print('Product saved')
            return False
        print('You need to press "a" or "b"')
