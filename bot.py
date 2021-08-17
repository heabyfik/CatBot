#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from service.facts import get_random_fact

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    message = fr'Привет, {user.mention_markdown_v2()}\!' + "\n\n"
    message += r"Я небольшой бот для любителей котиков и очень рад знакомству с тобой\." + "\n\n"
    message += r"Могу показать милых котиков, рассказать много интересных фактов и просто пообщаться с тобой, только попроси\." + "\n\n"
    message += r"Набери ```/help```, чтобы посмотреть мои команды\."

    update.message.reply_markdown_v2(message)


def fact_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /fact is issued."""
    update.message.reply_text(get_random_fact())


def cat_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /cat is issued."""
    update.message.reply_text("Этот функционал пока не готов")


def cute_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /cute is issued."""
    update.message.reply_text("Этот функционал пока не готов")


def story_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /story is issued."""
    update.message.reply_text("Этот функционал пока не готов")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    message = r"К вашим услугам\! Вот что я умею:" + "\n\n"
    message += r"```/fact``` \- расскажу интересный факт" + "\n"
    message += r"```/cat``` \- отправлю картинку котика" + "\n"
    message += r"```/cute``` \- отправлю милого котика^^" + "\n"
    message += r"```/story``` \- расскажу историю" + "\n"

    update.message.reply_markdown_v2(message)


def unknown_command(update: Update, context: CallbackContext) -> None:
    """Answer to unknown user command."""
    logging.info(update.message.text)
    message = r"Ой, а такой команды я не знаю\.\.\. Попробуй ```/help```\."

    update.message.reply_markdown_v2(message)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ.get("TELEGRAM_BOT_KEY"))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("fact", fact_command))
    dispatcher.add_handler(CommandHandler("cat", cat_command))
    dispatcher.add_handler(CommandHandler("cute", cute_command))
    dispatcher.add_handler(CommandHandler("story", story_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
