import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

logger = logging.getLogger(__name__)

ORDER = 'order'
YELLOW = 'Жовтий'
BEIGE = 'Кремовий'
BLACK = 'Чорний'
OLIVE = 'Оливковий'
PINK = 'Рожевий'
ORANGE = 'Помаранчевий'
GRAY = 'Сірий'
BLUE = 'Синій'


# first button
def reply_keyboard_order():
    reply_markup = [[InlineKeyboardButton('✏️ Оформити замовлення', callback_data=ORDER)]]
    return InlineKeyboardMarkup(reply_markup)


# cancel button
def reply_keyboard_cancel(CANCEL):
    reply_keyboard = [[InlineKeyboardButton('Скасувати', callback_data=CANCEL)]]
    return InlineKeyboardMarkup(reply_keyboard)


# amount buttons
def reply_keyboard_amount(CANCEL):
    reply_keyboard_amounts = [
        [InlineKeyboardButton('1', callback_data='1'),
         InlineKeyboardButton('2', callback_data='2'),
         InlineKeyboardButton('3', callback_data='3')],
        [InlineKeyboardButton('4', callback_data='4'),
         InlineKeyboardButton('5', callback_data='5'),
         InlineKeyboardButton('6', callback_data='6')],
        [InlineKeyboardButton('Скасувати', callback_data=CANCEL)]
    ]
    return InlineKeyboardMarkup(reply_keyboard_amounts)


# color buttons
def reply_keyboard_color(CANCEL):
    logger.info(f'CANCELPIC >>>{CANCEL}')
    reply_keyboard_colors = [
        [InlineKeyboardButton('Помаранчевий', callback_data=ORANGE),
         InlineKeyboardButton('Оливковий', callback_data=OLIVE),
         InlineKeyboardButton('Жовтий', callback_data=YELLOW)],
        [InlineKeyboardButton('Рожевий', callback_data=PINK),
         InlineKeyboardButton('Сірий', callback_data=GRAY),
         InlineKeyboardButton('Чорний', callback_data=BLACK)],
        [InlineKeyboardButton('Cиній', callback_data=BLUE),
         InlineKeyboardButton('Кремовий', callback_data=BEIGE)],
        [InlineKeyboardButton('Скасувати', callback_data=CANCEL)],
    ]
    return InlineKeyboardMarkup(reply_keyboard_colors)


# size buttons
def reply_keyboard_size(CANCEL):
    reply_keyboard_sizes = [
        [InlineKeyboardButton('35', callback_data='35'),
         InlineKeyboardButton('36-37', callback_data='36-37'),
         InlineKeyboardButton('38-39', callback_data='38-39')],
        [InlineKeyboardButton('40-41', callback_data='40-41'),
         InlineKeyboardButton('42-43', callback_data='42-43'),
         InlineKeyboardButton('44-45', callback_data='44-45')],
        [InlineKeyboardButton('Скасувати', callback_data=CANCEL)]
    ]
    return InlineKeyboardMarkup(reply_keyboard_sizes)
