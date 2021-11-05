import gspread
from google.oauth2.service_account import Credentials
from pydantic import BaseModel

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
    id: int
    title: str
    description: str
    price: float


def add_product(product):
     products_sheet.append_row(product)


def main():
    sample_product = Product(id=1, title='product 1', description="a product", price=0.1)
    product_values = list(sample_product.dict().values())
    add_product(product_values)

main()
