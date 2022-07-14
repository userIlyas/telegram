from telebot import TeleBot
import random
import threading
import time
from art import tprint

# authorization
bot = TeleBot('5366092082:AAHeFyp7ACouq973GQtBlYO2hZLxQEqK_pk')

# opening file "Viiseri.txt"
vis_lines = []
with open('viseri.txt') as file:
    for line in file:
        vis_lines.append(line)

# greetings
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет ✌")


# catching messages and answering
@bot.message_handler()
def start_message(message):
    global vis_lines

    # commands
    if message.text == 'срач':

        # random line from directory's file "viiseri.txt"
        mess = random.choice(vis_lines)
        bot.send_message(message.chat.id, mess)



    elif message.text == "Кто я":
        bot.send_message(message.chat.id, "Gay")

# working 24/7
def main():
    tprint("Bot working")
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()