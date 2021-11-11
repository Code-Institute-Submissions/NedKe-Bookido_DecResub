import gspread
from google.oauth2.service_account import Credentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import uuid
from gcalendar import add_event

SCOPES_SHEETS = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPES_SHEETS)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fartoor_products')
products_sheet = SHEET.worksheet('products')


class Product(BaseModel):
    id: str
    calendar_id: str
    title: str
    description: str
    address: str
    capacity: str
    price: str
    date: str
    time: str
    emails: str


class ProductRow(BaseModel):
    row_num: int
    product: Product


def add_product(product):
    product_values = list(product.dict().values())
    products_sheet.append_row(product_values)
    event = {
        'id': product.calendar_id,
        'summary': product.title,
        'location': product.address,
        'description': build_description(product.description, product.capacity, 0),
        'start': {
            'dateTime': convert_to_gcalendar_friendly_date(product.date,product.time),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': convert_to_gcalendar_friendly_date(product.date, (datetime.strptime(product.time, '%H:%M:%S') + timedelta(minutes=45)).strftime('%H:%M:%S')),
            'timeZone': 'America/Los_Angeles',
        }
    }
    add_event(event)


def convert_to_gcalendar_friendly_date(date, time):
    return f'{date}T{time}{GMT_OFF}'


def new_product_id():
    return str(len(products_sheet.get_all_records()))


def generate_calendar_id():
    return str(uuid.uuid4()).replace('-', '')


def list_products():
    products = products_sheet.get_all_records()
    return [ProductRow(row_num=i+2, product=Product(id=p['id'], calendar_id=p['calendar_id'], title=p['title'], description=p['description'], address=p['address'], capacity=p['capacity'], price=p['price'], date=p['date'], time=p['time'], emails=p['emails'])) for i, p in enumerate(products)]


def add_product_raw(title, description, address, price, capacity, date, time):
    calendar_id = generate_calendar_id()
    product_id = new_product_id()
    sample_product = Product(id=product_id, calendar_id=calendar_id, title=title, description=description, address=address, price=price, capacity=capacity, date=date, time=time, emails='')
    add_product(sample_product)
