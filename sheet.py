import gspread
from google.oauth2.service_account import Credentials
from pydantic import BaseModel
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


def new_product_id():
    return str(len(products_sheet.get_all_records()))

def generate_calendar_id():
    return str(uuid.uuid4()).replace('-', '')
