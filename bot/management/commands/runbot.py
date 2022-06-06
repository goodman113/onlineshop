from email.message import Message
from importlib.metadata import entry_points
from django.core.management.base import BaseCommand
from telegram.utils.request import Request
from telegram import Bot
from django.conf import settings
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CommandHandler,ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from bot.views import *


class Command(BaseCommand):
    help = 'Telegram-bot'



    def handle(self, *args, **options):
        request = Request(
            connect_timeout=None,
            read_timeout=None
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )

        updater = Updater(
            bot=bot,
            use_context=True
        )
        conv = ConversationHandler(
            entry_points=[
                 CommandHandler('start', start)
            ],
            states = {
                state_category:[
                MessageHandler(Filters.text, command_category)
                ],
                state_product:[
                MessageHandler(Filters.text, command_product)
                ]
            },
            fallbacks=[
                CommandHandler('start', start)
    ]
        )



        updater.dispatcher.add_handler(conv)
        updater.start_polling()
        updater.idle()
