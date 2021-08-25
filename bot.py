import os
import logging

from random import choice
from random import randint

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from service.facts import get_random_fact
from service.balaboba import get_random_story
from service.top_cat import get_random_top_cat_text
from service.top_cat import get_random_top_cat_photo

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
    message += r"Набери /help, чтобы посмотреть мои команды\."

    update.message.reply_markdown_v2(message)


def fact_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /fact is issued."""
    update.message.reply_text(get_random_fact())


def cat_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /cat is issued."""
    r = randint(0, 100000000)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=f"https://cataas.com/cat?_nocache={r}")


def cute_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /cute is issued."""
    r = randint(0, 100000000)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=f"https://cataas.com/cat/cute?_nocache={r}")


def funny_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /funny is issued."""
    r = randint(0, 100000000)
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=f"https://cataas.com/cat/cute?_nocache={r}",
                           caption=get_random_story(intro=choice([4, 4, 4, 8, 11])))


def story_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /story is issued."""
    update.message.reply_text(get_random_story(intro=choice([0, 6])))


def top_cat_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /top_cat is issued."""
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=get_random_top_cat_photo(),
                           caption=get_random_top_cat_text())


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    message = r"К вашим услугам\! Вот что я умею:" + "\n\n"
    message += r"/fact \- расскажу интересный факт" + "\n"
    message += r"/cat \- отправлю картинку котика" + "\n"
    message += r"/cute \- отправлю милого котика^^" + "\n"
    message += r"/story \- расскажу историю" + "\n"
    message += r"/funny \- попробую рассмешить" + "\n"
    message += r"/top\_cat \- покажу топового кота" + "\n"
    message += "\n"
    message += r"/about \- расскажу немного о себе" + "\n"

    update.message.reply_markdown_v2(message)


def about_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /about is issued."""
    message = r"Здорово, что вы заинтересовались\!" + "\n\n"
    message += r"Для отправки изображений я использую API [CATAAS](https://cataas.com/)\. "
    message += r"А для генерации текстов работает [Балабоба](https://yandex.ru/lab/yalm) от Яндекс, "
    message += r"поэтому не принимайте близко к сердцу то, о чём я рассказываю :\)" + "\n"
    message += "\n"
    message += r"Мой исходный код на гитхаб: https://github\.com/heabyfik/CatBot"

    update.message.reply_markdown_v2(message)


def unknown_command(update: Update, context: CallbackContext) -> None:
    """Answer to unknown user command."""
    logging.info(update.message.text)
    message = r"Ой, а такой команды я не знаю\.\.\. Попробуй /help"

    update.message.reply_markdown_v2(message)


def photo_handler(update: Update, context: CallbackContext) -> None:
    """Answer to photo upload."""
    for p in update.message.photo:
        print(p.get_file())
    message = r"Ой, а такой команды я не знаю\.\.\. Попробуй /help"

    update.message.reply_markdown_v2(message)


def main() -> None:
    """Start the bot."""
    updater = Updater(os.environ.get("TELEGRAM_BOT_KEY"))

    # get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    # control commands
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("about", about_command))
    # cat commands
    dispatcher.add_handler(CommandHandler("fact", fact_command))
    dispatcher.add_handler(CommandHandler("cat", cat_command))
    dispatcher.add_handler(CommandHandler("cute", cute_command))
    dispatcher.add_handler(CommandHandler("story", story_command))
    dispatcher.add_handler(CommandHandler("funny", funny_command))
    dispatcher.add_handler(CommandHandler("top_cat", top_cat_command))

    # on non command i.e message - print hint
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown_command))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
