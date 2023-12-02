import telebot

bot = telebot.TeleBot("5142077483:AAEPrYHJ4kMlWD4Ixvbn7U8Aw9QgV14Wfc0")

@bot.message_handler()
def reply(message):
    bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.infinity_polling()