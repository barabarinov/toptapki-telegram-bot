import os
import logging
from dotenv import load_dotenv

from telegram.ext import (
    Updater,
    CommandHandler,
)

from app.handlers.start import start
from app.handlers.ordering import ordering_conversation_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    load_dotenv()

    IS_HEROKU = os.getenv('IS_HEROKU', 'true').lower() == 'true'

    PORT = int(os.environ.get('PORT', 5000))
    TOKEN = os.getenv('TOKEN')

    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(ordering_conversation_handler)

    if IS_HEROKU:
        updater.start_webhook(
                            listen="0.0.0.0",
                            port=PORT,
                            url_path=TOKEN,
                            webhook_url=f'https://toptapki-telegtam-bot.herokuapp.com/{TOKEN}'
        )
    else:
        updater.start_polling()
    updater.idle()
