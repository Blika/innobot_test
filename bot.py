#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import logging

import telegram
from telegram.ext import Updater, CommandHandler

from models import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def book_create(update, context):
    msg: telegram.Message = update.message
    text: str = msg.text
    done = text.split()
    del (done[0])
    if len(done) < 1:
        update.message.reply_text("You must type the id of the book.")
        return

    donev = ""
    for e in done:
        donev += " " + e

    query = Book.select().where(Book.name == donev)
    if query.exists():
        update.message.reply_text("This book already exists!")
        return

    book = Book.create(name=donev)
    id = book.get_id()
    update.message.reply_text(f"{donev} has successfully been created. Its id is {id}")


def delete_book(update, context):
    msg: telegram.Message = update.message
    text: str = msg.text
    done = text.split()
    del (done[0])

    if len(done) < 1:
        update.message.reply_text("You must type the id of the book.")
        return

    donev = ""
    for e in done:
        donev += " " + e

    try:
        int(donev)
    except ValueError:
        update.message.reply_text("Arguments must be integer")
        return

    donev = int(donev)

    try:
        Book.get_by_id(donev)
    except peewee.DoesNotExist:
        update.message.reply_text("This book does not exist!")
        return

    update.message.reply_text(f"{donev} has successfully been deleted")
    Book.delete_by_id(donev)


def get_book(update, context):
    msg: telegram.Message = update.message
    text: str = msg.text
    done = text.split()
    del (done[0])

    if len(done) < 1:
        update.message.reply_text("You must type the id of the book.")
        return

    donev = ""
    for e in done:
        donev += " " + e

    try:
        int(donev)
    except ValueError:
        update.message.reply_text("Arguments must be integer")
        return

    donev = int(donev)

    try:
        Book.get_by_id(donev)
    except peewee.DoesNotExist:
        update.message.reply_text("This book does not exist!")
        return

    book = Book.get_by_id(donev)
    update.message.reply_text(f"This book named {book.name}")


def find_book(update, context):
    msg: telegram.Message = update.message
    text: str = msg.text
    done = text.split()
    del (done[0])

    if len(done) < 1:
        update.message.reply_text("You must type the text.")
        return

    donev = ""
    for e in done:
        donev += " " + e

    book = Book.select().where(Book.name.contains(donev))
    if not book.exists():
        update.message.reply_text("This book does not exist!")
        return
    newbook = Book.get_by_id(book.get())
    update.message.reply_text(f"This book named {newbook.name}. Its id is {book.get()}")


def update_book(update, context):
    msg: telegram.Message = update.message
    text: str = msg.text
    done = text.split()
    del (done[0])

    if len(done) < 1:
        update.message.reply_text("You must type the id of the book.")
        return

    if len(done) < 2:
        update.message.reply_text("You must type the new name of the book.")
        return

    donev = done[0]
    try:
        int(donev)
    except ValueError:
        update.message.reply_text("ID must be integer")
        return

    donev = int(donev)

    try:
        Book.get_by_id(donev)
    except peewee.DoesNotExist:
        update.message.reply_text("This book does not exist!")
        return

    book = Book.get_by_id(donev)
    book.name = done[1]
    book.save()
    update.message.reply_text(f"This book has been named as {done[1]}")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("create", book_create))
    dp.add_handler(CommandHandler("delete", delete_book))
    dp.add_handler(CommandHandler("get", get_book))
    dp.add_handler(CommandHandler("update", update_book))
    dp.add_handler(CommandHandler("search", find_book))
    dp.add_error_handler(error)
    if config.HEROKU_APP_NAME is None:
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",
                              port=config.PORT,
                              url_path=config.TOKEN)
        updater.bot.set_webhook(f"https://{config.HEROKU_APP_NAME}.herokuapp.com/{config.TOKEN}")

    updater.idle()


if __name__ == '__main__':
    main()
