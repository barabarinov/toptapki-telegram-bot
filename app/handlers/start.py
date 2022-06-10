from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from app.texts import hello_text
from app.buttons import reply_keyboard_order


def start(update: Update, context: CallbackContext):
    update.message.reply_video(
        video=open('pics/toptapki_4.mp4', 'rb'),
        caption=hello_text,
        reply_markup=reply_keyboard_order(),
        parse_mode=ParseMode.MARKDOWN,
    )
