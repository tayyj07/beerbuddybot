import sqlite3
import datetime as dt

conn = sqlite3.connect('bot_db.db', check_same_thread=False)
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS database (datetime , user BLOB, item TEXT, item_qty INTEGER, item_price FLOAT, friends_qty INTEGER)')

def user_entry(user):
    date = dt.datetime.now()
    c.execute('INSERT INTO database (datetime, user) VALUES (?, ?)',
              (date, user))
    conn.commit()

def update_user_menu(user, item):
    c.execute('UPDATE database SET item = (?) WHERE user = (?) ORDER BY datetime DESC LIMIT 1',
              (item, user))
    conn.commit()

def update_user_qty(user, qty):
    c.execute('UPDATE database SET item_qty = (?) WHERE user = (?) ORDER BY datetime DESC LIMIT 1',
              (qty, user))
    conn.commit()

def update_user_price(user,price):
    c.execute('UPDATE database SET item_price = (?) WHERE user = (?) ORDER BY datetime DESC LIMIT 1',
              (price, user))
    conn.commit()

def update_user_friends(user, friends):
    c.execute('UPDATE database SET friends_qty = (?) WHERE user = (?) ORDER BY datetime DESC LIMIT 1',
              (friends, user))
    conn.commit()

def receipt(user):
    row = c.execute('SELECT * FROM database WHERE user = (?) ORDER BY datetime DESC LIMIT 1', (user,)).fetchall()
    receipt_txt = '#######\n' \
                  'Datetime: {0}\n' \
                  'Item ordered: {1}\n' \
                  'Quantity: {2}\n' \
                  'Unit price: {3}\n' \
                  'Total bill of {4} to split between {5} people\n' \
                  'Each person is to pay {6}\n' \
                  '#######'.format(row[0][0][:19], row[0][2], row[0][3], row[0][4], row[0][3] * row[0][4], row[0][5], row[0][3] * row[0][4] / row[0][5])

    return receipt_txt

def price_check(user):
    row = c.execute('SELECT * FROM database WHERE user = (?) ORDER BY datetime DESC LIMIT 1', (user,)).fetchall()
    if row[0][2] and row[0][3] is not None:
        if row[0][4] is None:
            return True
        elif row[0][4] is not None:
            return False
    elif row[0][2] or row[0][3] is None:
        return False
