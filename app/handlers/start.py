from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from app.texts import hello_text
from app.buttons import reply_keyboard_order


def start(update: Update, context: CallbackContext):
    update.message.reply_animation(
        animation=open('pics/toptapki_1.gif', 'rb'),
        caption=hello_text,
        reply_markup=reply_keyboard_order(),
        parse_mode=ParseMode.MARKDOWN,
    )
