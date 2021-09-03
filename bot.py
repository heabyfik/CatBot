import os
import time
import logging

from random import choice
from random import randint

import telegram.error
from telegram import Update
from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from storage import Photo
from storage import add_photo
from storage import get_random_photo

from service.facts import get_random_fact
from service.balaboba import get_random_story
from service.http_cats import get_http_cat
from service.http_cats import is_valid_status_code
from service.top_cat import get_random_top_cat_text
from service.top_cat import get_random_top_cat_photo

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

BAD_REQUEST = "Отправка изображений временно недоступна, попробуйте пока другую команду. Вот список: /help"


def log(func):
    """Logging decorator."""

    def wrap(update: Update, context: CallbackContext):
        start = time.time()
        result = func(update, context)
        end = time.time()

        logger.info(f"{func.__name__} [{update.effective_user.username}]: {update.message.text} ({end - start})")

        return result

    return wrap


temp_storage = {}


@log
def start_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    message = fr'Привет, {user.mention_markdown_v2()}\!' + "\n\n"
    message += r"Я небольшой бот для любителей котиков и очень рад знакомству с тобой\." + "\n\n"
    message += r"Могу показать милых котиков, рассказать много интересных фактов и просто пообщаться с тобой, только попроси\." + "\n\n"
    message += r"Набери /help, чтобы посмотреть мои команды\."

    update.message.reply_markdown_v2(message)


@log
def fact_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /fact is issued."""
    update.message.reply_text(get_random_fact())


@log
def cat_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /cat is issued."""
    try:
        r = randint(0, 100000000)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=f"https://cataas.com/cat?_nocache={r}")
    except telegram.error.BadRequest:
        update.message.reply_text(BAD_REQUEST)


@log
def cute_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /cute is issued."""
    try:
        r = randint(0, 100000000)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=f"https://cataas.com/cat/cute?_nocache={r}")
    except telegram.error.BadRequest:
        update.message.reply_text(BAD_REQUEST)


@log
def funny_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /funny is issued."""
    try:
        r = randint(0, 100000000)
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=f"https://cataas.com/cat/cute?_nocache={r}",
                               caption=get_random_story(intro=choice([4, 4, 4, 8, 11])))
    except telegram.error.BadRequest:
        update.message.reply_text(BAD_REQUEST)


@log
def story_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /story is issued."""
    update.message.reply_text(get_random_story(intro=choice([0, 6])))


@log
def top_cat_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /top_cat is issued."""
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=get_random_top_cat_photo(),
                           caption=get_random_top_cat_text())


@log
def http_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /http is issued."""
    c = update.message.text.split(' ')
    if len(c) != 2:
        message = "Формат команды: /http <status_code>"
        update.message.reply_text(message)
        return

    try:
        status_code = int(c[1])
        if not is_valid_status_code(status_code):
            message = r"Такого кода я не знаю\." + "\n\n" + r"Попробуйте `/http 200`"
            update.message.reply_markdown_v2(message)
            return
        else:
            p = get_http_cat(status_code)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=p)

    except ValueError as e:
        message = r"Не могу разобрать\." + "\n\n" + r"Попробуйте `/http 200`"
        update.message.reply_markdown_v2(message)


@log
def gallery_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /gallery is issued."""
    photo: Photo = get_random_photo()
    context.bot.send_photo(chat_id=update.effective_chat.id,
                           photo=photo.file_id,
                           caption=photo.description)


@log
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    message = r"К вашим услугам\! Вот что я умею:" + "\n\n"
    message += r"/fact \- расскажу интересный факт" + "\n"
    message += r"/cat \- отправлю картинку котика" + "\n"
    message += r"/cute \- отправлю милого котика^^" + "\n"
    message += r"/story \- расскажу историю" + "\n"
    message += r"/funny \- попробую рассмешить" + "\n"
    message += r"/top\_cat \- покажу топового кота" + "\n"
    message += r"/http \<status\_code\> \- HTTP\-кот" + "\n"
    message += "\n"
    message += r"/gallery \- покажу кота из коллекции" + "\n"
    message += r"/upload \- добавляю вашего котика" + "\n"
    message += "\n"
    message += r"/about \- расскажу немного о себе" + "\n"

    update.message.reply_markdown_v2(message)


@log
def about_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /about is issued."""
    message = r"Здорово, что вы заинтересовались\!" + "\n\n"
    message += r"Для отправки изображений я использую API [CATAAS](https://cataas.com/) и [HTTP Cats](https://http.cat/)\. "
    message += r"А для генерации текстов работает [Балабоба](https://yandex.ru/lab/yalm) от Яндекс, "
    message += r"поэтому не принимайте близко к сердцу то, о чём я рассказываю :\)" + "\n"
    message += "\n"
    message += r"Мой исходный код на гитхаб: https://github\.com/heabyfik/CatBot"

    update.message.reply_markdown_v2(message)


@log
def unknown_command(update: Update, context: CallbackContext) -> None:
    """Answer to unknown user command."""
    logging.info(update.message.text)
    message = r"Ой, а такой команды я не знаю\.\.\. Попробуй /help"

    update.message.reply_markdown_v2(message)


# for conversation
PHOTO, DESCRIPTION = range(2)


@log
def conversation_start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks for photo upload."""
    update.message.reply_text(
        'Вы решили рассказать про своего питомца? Очень здорово!\n\n' +
        'Отправляйте фото своего пушистика прямо сюда.\n\n' +
        'Или отправьте /cancel чтобы завершить диалог.'
    )

    return PHOTO


@log
def conversation_photo(update: Update, context: CallbackContext) -> int:
    """Handles photo upload."""
    photo = update.message.photo[-1].get_file()
    temp_storage[update.effective_chat.id] = photo.file_id
    update.message.reply_text('Супер! Теперь вы можете немного про него рассказать, а я всё это сохраню.')

    return DESCRIPTION


@log
def conversation_description(update: Update, context: CallbackContext) -> int:
    """Stores the info about cat."""
    chat_id = update.effective_chat.id
    file_id = temp_storage.get(chat_id, "")
    description = update.message.text

    p = Photo(file_id, chat_id, description)
    add_photo(p)

    temp_storage.pop(chat_id, None)
    update.message.reply_text(
        'Отлично! Теперь ваш питомец тоже в моей коллекции.\n\n' +
        'Чтобы продолжить общение наберите /help'
    )

    return ConversationHandler.END


@log
def conversation_cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    update.message.reply_text('Хорошо. Надеюсь, вы поделитесь со мной в следующий раз.')

    return ConversationHandler.END


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
    dispatcher.add_handler(CommandHandler("http", http_command))
    dispatcher.add_handler(CommandHandler("top_cat", top_cat_command))
    dispatcher.add_handler(CommandHandler("gallery", gallery_command))

    # Photo upload conversation
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('upload', conversation_start)],
        states={
            PHOTO: [MessageHandler(Filters.photo, conversation_photo)],
            DESCRIPTION: [MessageHandler(Filters.text & ~Filters.command, conversation_description)],
        },
        fallbacks=[CommandHandler('cancel', conversation_cancel)],
    )
    dispatcher.add_handler(conv_handler)

    # on non command i.e message - print hint
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, unknown_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
