import logging
import gspread
import json
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)

load_dotenv()

gc = gspread.service_account_from_dict(json.loads(os.getenv('CREDENTIALS')))

sh = gc.open("toptapki")
wks = sh.worksheet('Замовлення')


def send_information_to_google_sheets(update: Update, context: CallbackContext):
    wks.insert_rows(
        values=[
            [context.user_data['user_name'],
             context.user_data['phone_number'],
             context.user_data['amount'],
             context.user_data['color'].lstrip(', '),
             context.user_data['size'].lstrip(', '),
             context.user_data['postal_address'],
             ]
        ], row=2)
    logging.info('✅ Google SpreadSheet has been filled!')
