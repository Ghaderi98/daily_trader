# -*- coding: utf-8 -*-
"""Daily_Trader.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hWUOGLOusVHvtnUqhspP-EDxWWdy052o
"""

import os
import yfinance as yf
import schedule
import time
from telegram.ext import Updater, CommandHandler

# Function to perform daily trading for the specified symbol
def perform_daily_trade(symbol):
    stock_data = yf.download(symbol, period='1d')
    if stock_data.empty:
        return f"Sorry, we could not find any data for {symbol}."
    # Write your code here to perform daily trading for the specified symbol
    # ...
    return f"Daily trading for {symbol} has been completed successfully."

# Function to start the bot
def start(update, context):
    user = update.message.from_user
    context.user_data['user_id'] = user.id  # Save user ID in context.user_data
    context.user_data['username'] = user.username  # Save username in context.user_data
    update.message.reply_text(f'Welcome to my trading bot, {user.first_name}! Your user ID is {user.id}. Use /trading_signals to get started.')

# Function to get trading signals
def trading_signals(update, context):
    update.message.reply_text('Here are the latest trading signals: ...')

def main():
    # Get bot token from environment variable
    bot_token = os.environ.get('6267175686:AAGzZZlJMwrIEsdv_ijXBwZvJqNu_nMkA_A')
    if not bot_token:
        print('Please set the TELEGRAM_BOT_TOKEN environment variable.')
        return

    updater = Updater(token=bot_token, use_context=True)

    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    trading_signals_handler = CommandHandler('trading_signals', trading_signals)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(trading_signals_handler)

    updater.start_polling()

    # Schedule daily trade for each symbol
    symbols = ['AAPL', 'MSFT', 'AMZN','GOOGL','YHOO'] # Add your symbols here
    for symbol in symbols:
        schedule.every().day.at("09:00").do(lambda: updater.bot.send_message(chat_id='@my_channel', text=perform_daily_trade(symbol)))

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()