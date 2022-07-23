from telebot import TeleBot
import random
from art import tprint
import sqlite3
import traceback

# authorization
bot = TeleBot('5366092082:AAHeFyp7ACouq973GQtBlYO2hZLxQEqK_pk')
con = sqlite3.connect('mydatabase.db', check_same_thread=False)
c = con.cursor()
if c.execute(f"""SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users';"""):
    print("Table is available")
    con.commit()
else:
    print("There is no table... creating")
    c.execute(
    """CREATE TABLE users(user_id integer PRIMARY KEY, user_name text, user_surname text, username text)""")
    con.commit()


# opening file "Visser.txt"
vis_lines = []
with open('viseri.txt') as file:
    for line in file:
        vis_lines.append(line)


# updating info about user
def sql_update(user_id: int, param: str, value: str):
    global c, con
    c.execute(f"UPDATE users SET {param} = '{value}' where user_id = {user_id}")
    con.commit()
    print("sql_update is performed")


# adding user
def sql_insert(user_id: int, user_name: str, user_surname: str, username: str):
    global c, con
    if c.execute(f"""SELECT user_name FROM users WHERE user_id='{user_id}'"""):
        pass
    else:
        c.execute(f"""INSERT INTO users(user_id ,user_name ,user_surname ,
                username ) VALUES({user_id}, '{user_name}', '{user_surname}', '{username}')""")
        con.commit()
        print("sql_insert is performed")


# get info(to user)
def get_info(user_id):
    global c, con
    user_name = c.execute(
        f"SELECT user_name from users WHERE user_id = {user_id}"
    ).fetchall()[0][0]
    user_surname = c.execute(
        f"SELECT user_surname from users WHERE user_id = {user_id}"
    ).fetchall()[0][0]
    username = c.execute(
        f"SELECT username from users WHERE user_id = {user_id}"
    ).fetchall()[0][0]
    print("get_info is performed", user_name, user_surname, username)
    return [user_name, user_surname, username]


# greetings
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hi ✌")


# catching messages and answering
@bot.message_handler()
def start_message(message):
    global vis_lines

    # commands
    if message.text == "срач":

        # random line from directory's file "viiseri.txt"
        if message.chat.last_name is not None:
            mess = f"{message.chat.first_name} {message.chat.last_name}, {random.choice(vis_lines)}"
        else:
            mess = f"{message.chat.first_name}, {random.choice(vis_lines)}"

        bot.send_message(message.chat.id, mess)
        print(f"{message.chat.username} sent by {message.text} message_to: {mess} ")

    elif message.text == "add":
        sql_insert(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username)
        bot.send_message(message.chat.id, "You was added!")

    elif message.text == "check":
        try:
            user_name, user_surname, username = get_info(message.chat.id)
            bot.send_message(message.chat.id, f"Your user_name: {user_name}\n"
                                              f"Your user_surname {user_surname}\n"
                                              f"Your username {username}\n"
                                              f"Right? If false send: 'update'")
        except:
            bot.send_message(message.chat.id, f"Error\n"
                                              f"{traceback.format_exc()}")

    elif message.text == "update":
        try:
            sql_update(message.chat.id, "user_name", message.chat.first_name)
            sql_update(message.chat.id, "user_surname", message.chat.last_name)
            bot.send_message(message.chat.id, "Parameters has been updated!")
        except Exception as er:
            bot.send_message(message.chat.id, f"Error\n"
                                              f"{traceback.format_exc()}")


# working 24/7
def main():
    tprint("Bot working")
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()