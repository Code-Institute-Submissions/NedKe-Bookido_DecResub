"""
sheet module contains settings and methods to create new product and also
add bookings to the already creating products
"""


from datetime import datetime, timedelta
import uuid
import gspread
from google.oauth2.service_account import Credentials
from pydantic import BaseModel
from gcalendar import add_event, update_event_description


SCOPES_SHEETS = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPES_SHEETS)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('bookido')
products_sheet = SHEET.worksheet('products')

GMT_OFF = '+01:00'


class Product(BaseModel):
    """Product model holding information about a prouduct in the application"""
    id: str
    calendar_id: str
    title: str
    description: str
    address: str
    capacity: str
    price: str
    duration: str
    date: str
    time: str
    emails: str


class ProductRow(BaseModel):
    """Product row model storing row_num to access product row in the sheet"""
    row_num: int
    product: Product


def convert_to_gcalendar_friendly_date(date, time):
    """
    Converts date and time parameters to Google calendar friendly format
    :param date: date of an event
    :param time: time of an event
    """
    return f'{date}T{time}{GMT_OFF}'


class CapacityReachedException(Exception):
    """
    Exception to be thrown when capacity is reached while booking a product
    """
    pass


class ProductNotFoundException(Exception):
    """
    Exception to be thrown when a product not found in the list of products
    """
    pass


class CustomerAlreadyRegistered(Exception):
    """
    Exception to be thrown when a customer has already booked a product
    """
    pass


def add_booking(product_id, email):
    """
    Creates a booking for a product by adding customer's email to the datastore
    and creating an Google calendar event based on product timing

    :param product_id: product to be booked
    :param email: customer's email
    """

    product_row = get_product_row(product_id)
    product = product_row.product
    emails = product.emails.split(',') if product.emails != '' else []
    if email in emails:
        raise CustomerAlreadyRegistered
    if len(emails) > int(product.capacity) - 1:
        raise CapacityReachedException("capacity reached")
    emails.append(email)

    emails_to_store = email if len(emails) == 1 else ','.join(emails)
    emails_row = 11
    products_sheet.update_cell(
        product_row.row_num,
        emails_row,
        emails_to_store)
    description = build_description(product.description, product.capacity,
                                    len(emails))
    description += '\n' + '\n'.join(emails_to_store.split(','))
    update_event_description(product.calendar_id, description)


def build_description(product_description, product_capacity, num_booked):
    """
    Builds the description for the summary section of Google calendar event
    :param product_description: description of a product
    :param product_capacity: capacity of the product
    :param num_booked: the number of booked customers to be shown in calendar
    """
    return f'{product_description} ({num_booked}/{product_capacity})'


def add_product(product):
    """
    Persists a product in Google sheet and creates an event in Goole calendar
    :param product:  Product that is added by admins
    """
    product_values = list(product.dict().values())
    products_sheet.append_row(product_values)
    event = {
        'id': product.calendar_id,
        'summary': product.title,
        'location': product.address,
        'description': build_description(product.description, product.capacity,
                                         0),
        'start': {
            'dateTime': convert_to_gcalendar_friendly_date(product.date,
                                                           product.time),
            'timeZone': 'Europe/Stockholm',
        },
        'end': {
            'dateTime': convert_to_gcalendar_friendly_date(product.date, (
                datetime.strptime(product.time, '%H:%M:%S') + timedelta(
                    minutes=45)).strftime('%H:%M:%S')),
            'timeZone': 'Europe/Stockholm',
        }
    }
    add_event(event)


def generate_calendar_id():
    """Generates Calendar id to for Google calendar events"""

    return str(uuid.uuid4()).replace('-', '')


def generate_new_product_id():
    """
    Generates a unique id for a product based on the already saved
    records in the Google spreadsheet
    """
    return str(len(products_sheet.get_all_records()))


def list_products():
    """Deserializes all prducts inito ProductRow model"""
    products = products_sheet.get_all_records()

    product_rows = [ProductRow(row_num=i + 2,
                               product=Product(id=p['id'],
                                               calendar_id=p['calendar_id'],
                                               title=p['title'],
                                               description=p['description'],
                                               address=p['address'],
                                               capacity=p['capacity'],
                                               price=p['price'],
                                               duration=p['duration'],
                                               date=p['date'], time=p['time'],
                                               emails=p['emails'])) for i, p in
                    enumerate(products)]

    return list(
        filter(
            lambda p: datetime.strptime(
                f'{p.product.date} {p.product.time}',
                '%Y-%m-%d %H:%M:%S') > datetime.now(),
            product_rows))


def get_product_row(product_id):
    """
    Returns the product found in the list of products using product_id
    :param product_id
    """
    for product_row in list_products():
        if product_row.product.id == product_id:
            return product_row
    raise ProductNotFoundException("product not found")


def add_product_raw(
        title,
        description,
        address,
        price,
        capacity,
        duration,
        date,
        time):
    """
    Creates a new product model and stores it using add_product method
    :param title
    :param description
    :param address
    :param price
    :param capacity
    :param duration
    :param date
    :param time
    """
    calendar_id = generate_calendar_id()
    product_id = generate_new_product_id()
    new_product = Product(
        id=product_id,
        calendar_id=calendar_id,
        title=title,
        description=description,
        address=address,
        capacity=capacity,
        price=price,
        duration=duration,
        date=date,
        time=time,
        emails='')
    add_product(new_product)
