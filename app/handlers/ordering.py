import logging
from enum import auto, IntEnum
from telegram import Update, ParseMode
from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CallbackContext,
)
from app.gsheet import send_information_to_google_sheets
from app.texts import (
    name,
    number,
    amount,
    color,
    colors,
    size,
    address,
    order_accepted,
    good_luck,
)
from app.buttons import (
    reply_keyboard_cancel,
    reply_keyboard_amount,
    reply_keyboard_color,
    reply_keyboard_size,
)

logger = logging.getLogger(__name__)

ORDER = 'order'
CANCEL = 'cancel'
CANCELPIC = 'cancelpic'
NUMBERS = '1|2|3|4|5|6'
COLORS = 'Жовтий|Помаранчевий|Чорний|Оливковий|Рожевий|Кремовий|Сірий|Синій'
SIZES = '35|36-37|38-39|40-41|42-43|44-45'


class NewOrder(IntEnum):
    NAME = auto()
    NUMBER = auto()
    AMOUNT = auto()
    COLOR = auto()
    SIZE = auto()
    POSTAL_ADDRESS = auto()


def new_order(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text=name,
        reply_markup=reply_keyboard_cancel(CANCEL),
    )

    return NewOrder.NAME


def get_name(update: Update, context: CallbackContext):
    context.user_data['user_name'] = update.message.text
    logger.info(f'USER NAME >>> {context.user_data["user_name"]}')

    update.message.reply_text(
        text=number,
        reply_markup=reply_keyboard_cancel(CANCEL),
    )

    return NewOrder.NUMBER


def get_phone_number(update: Update, context: CallbackContext):
    context.user_data['phone_number'] = update.message.text
    logger.info(f'PHONE NUMBER >>> {context.user_data["phone_number"]}')

    update.message.reply_text(
        text=amount,
        reply_markup=reply_keyboard_amount(CANCEL),
    )
    context.user_data['item_amount'] = 0

    return NewOrder.AMOUNT


def get_amount(update: Update, context: CallbackContext):
    logger.info("I'm in get amount!")
    query = update.callback_query
    context.user_data['amount'] = query.data
    # query.answer(text='HELLO', show_alert=True)
    logger.info(f'AMOUNT >>> {context.user_data["amount"]}')
    item_amount = context.user_data['item_amount']

    if context.user_data['item_amount'] < int(context.user_data['amount']):
        context.bot.send_photo(
            chat_id=query.message.chat_id,
            caption=colors.format(item_amount + 1),
            photo=open('pics/colors.png', 'rb'),
            reply_markup=reply_keyboard_color(CANCEL),
        )
        #
        # context.user_data['color'] = query.data
        logger.info(f'WHAT IN QUERY.DATA >>> {query.data}')

        logger.info(f'ITEM AMOUNT >>> {context.user_data["item_amount"]}')
        # return NewOrder.AMOUNT

        return NewOrder.COLOR

    # else:
    #     query.answer()
    #     context.bot.send_photo(
    #         chat_id=query.message.chat_id,
    #         photo=open('pics/colors.png', 'rb'),
    #         caption=color,
    #         reply_markup=reply_keyboard_color(CANCEL),
    #     )
    #
    #     return NewOrder.COLOR


def get_color(update: Update, context: CallbackContext):
    query = update.callback_query
    logger.info(f'QUERY DATA AFTER >>> {query.data}')
    context.user_data['color'] = ''
    context.user_data['color'] += query.data

    logger.info(f'COLOR >>> {context.user_data["color"]}')
    query.answer()

    context.bot.send_message(
        chat_id=query.message.chat_id,
        text=size,
        reply_markup=reply_keyboard_size(CANCEL),
        )

    return NewOrder.SIZE


def get_size(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data['size'] = query.data
    query.answer(text='GET_SIZE')
    logger.info(f'SIZE >>> {context.user_data["size"]}')
    context.user_data['item_amount'] += 1
    logger.info(f'ITEM AMOUNT +1 >>> {context.user_data["item_amount"]}')
    if context.user_data['item_amount'] < int(context.user_data['amount']):
        return NewOrder.AMOUNT
    else:
        query.answer()

        context.bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text=address,
            disable_web_page_preview=True,
            reply_markup=reply_keyboard_cancel(CANCEL),
            parse_mode=ParseMode.MARKDOWN,
        )

        return NewOrder.POSTAL_ADDRESS


def get_postal_address(update: Update, context: CallbackContext):
    context.user_data['postal_address'] = update.message.text
    logger.info(f'Context.user_data >>> {context.user_data} <<<')
    logger.info(f'POSTAL ADDRESS >>> {context.user_data["postal_address"]}')

    send_information_to_google_sheets(update, context)

    update.message.reply_text(
        text=order_accepted,
        parse_mode=ParseMode.MARKDOWN,
    )

    return ConversationHandler.END


def cancel_conversation(update: Update, context: CallbackContext):
    query = update.callback_query
    logger.info(f'CALLBACK_QUERY >>> {query}')
    query.answer()

    context.bot.send_message(
        chat_id=query.message.chat_id,
            text=good_luck,
    )

    return ConversationHandler.END


ordering_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(new_order, pattern=ORDER)],
    states={
        NewOrder.NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
        NewOrder.NUMBER: [MessageHandler(Filters.text & ~Filters.command, get_phone_number)],
        NewOrder.AMOUNT: [CallbackQueryHandler(get_amount, pattern=NUMBERS)],
        NewOrder.COLOR: [CallbackQueryHandler(get_color, pattern=COLORS)],
        NewOrder.SIZE: [CallbackQueryHandler(get_size, pattern=SIZES)],
        NewOrder.POSTAL_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, get_postal_address)],
    },
    fallbacks=[
        CallbackQueryHandler(cancel_conversation, pattern=CANCEL),
    ],
)
