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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import config
import models

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

message_count = 1


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hello!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('What can I do for you?')


def save(update, context):
    msg: telegram.Message = update.message

    user, created = models.User.get_or_create(
        tg_id=msg.from_user.id,
        defaults={
            "full_name": msg.from_user.full_name
        }
    )

    models.Message.create(
        message_id=msg.message_id,
        chat_id=msg.chat_id,
        text=msg.text,
        user=user
    )


def last(update, context):
    last = 10
    if len(context.args) > 0:
        last = int(context.args[0])
    msg: telegram.Message = update.message
    for msg2 in models.Message.filter(chat_id=msg.chat_id).order_by(models.Message.id.desc()).limit(last):
        update.message.reply_text(msg2.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("last", last))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, save))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if config.HEROKU_APP_NAME is None:
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0",
                              port=config.PORT,
                              url_path=config.TOKEN)
        updater.bot.set.web_hook(f"https://{config.HEROKU_APP_NAME}.herokuapp.com/{config.TOKEN}")

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
