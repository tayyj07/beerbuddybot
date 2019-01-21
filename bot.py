from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from os import environ

import bot_db as db

db.create_table()

bot = TeleBot(environ['TELEGRAM_TOKEN'])

text_messages = {
    'start':
        u'Hello there! This is your Beer Buddy\n'
        u'What did you order?',

    'info':
        u'I am a bot that helps to split your bills'
}

def menu_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton(text='Beer Tower',
                                    callback_data='menu_Beer Tower'),
               InlineKeyboardButton(text='Truffle Fries',
                                    callback_data='menu_Truffle Fries'))
    return markup

def menu_qty_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    for i in range(1,10):
        markup.add(InlineKeyboardButton(text=i,
                                        callback_data='qty_{0}'.format(i)))
    return markup

def friends_qty_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    for i in range(1,10):
        markup.add(InlineKeyboardButton(text=i,
                                        callback_data='friends_{0}'.format(i)))
    return markup


@bot.message_handler(commands=['start'])
def start_bot(message):
    db.user_entry(message.chat.id)
    bot.reply_to(message, text_messages['start'])
    bot.send_message(chat_id=message.chat.id,
                     text="What did you order?",
                     reply_markup=menu_markup())

@bot.message_handler(commands=['info'])
def get_inf(message):
    bot.reply_to(message, text_messages['info'])



@bot.callback_query_handler(func=lambda call:True)
def callback_query(call):
    if call.data.startswith('menu'):
        db.update_user_menu(call.message.chat.id,call.data[5:])
        bot.send_message(chat_id=call.message.chat.id,
                         text='How many did you buy?',
                         reply_markup=menu_qty_markup())

    if call.data.startswith('qty'):
        db.update_user_qty(call.message.chat.id,call.data[4:])
        bot.send_message(chat_id=call.message.chat.id,
                         text='Please enter price of item')

    if call.data.startswith('friends'):
        db.update_user_friends(call.message.chat.id,call.data[8:])
        bot.send_message(chat_id=call.message.chat.id,
                         text=db.receipt(call.message.chat.id))


@bot.message_handler(content_types=['text'])
def messagehandler_price(message):
    try:
        if db.price_check(message.chat.id) is True:
            try:
                db.update_user_price(message.chat.id, float(message.text))
                bot.send_message(chat_id=message.chat.id,
                                 text='How many people are sharing?',
                                 reply_markup=friends_qty_markup())
            except Exception as e:
                print(e)
                bot.reply_to(message=message,
                             text='Please enter a valid price!\n(eg. 24.99)')
        else:
            bot.send_message(chat_id=message.chat.id,
                             text='You have an incomplete split bill request. Please complete the current process or type /start to restart!')
    except Exception as e:
        print(e)

bot.polling(timeout=100)
