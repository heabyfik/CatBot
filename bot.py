import os
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from service.facts import get_random_fact

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


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
    updater = Updater(os.environ.get("TELEGRAM_BOT_KEY"))

    # get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("fact", fact_command))
    dispatcher.add_handler(CommandHandler("cat", cat_command))
    dispatcher.add_handler(CommandHandler("cute", cute_command))
    dispatcher.add_handler(CommandHandler("story", story_command))
    # on non command i.e message - print hint
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
