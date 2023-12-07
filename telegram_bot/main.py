from enum import Enum

import requests
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, ContextTypes, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

class Bot(Enum):
    VOLK='Волк'
    PUSHKIN='Пушкин'

TEXT_GENERATOR_URL='http://basic-text-generator-text_generator-1:5001/generate'
BOT_TOKEN="5142077483:AAEPrYHJ4kMlWD4Ixvbn7U8Aw9QgV14Wfc0"
current_bot=Bot.VOLK


async def reply_with_model_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt=update.message.text
    json_reply = requests.post(TEXT_GENERATOR_URL, json={"prompts": prompt}).json()
    reply = json_reply[0]["generated_text"]
    await update.message.reply_text(reply)

async def choose_model_menu(update, context):
    keyboard = [
        [InlineKeyboardButton('Бот Bолк', callback_data=Bot.VOLK.name)],
        [InlineKeyboardButton('Бот Пушкин', callback_data=Bot.PUSHKIN.name)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выберите одну из доступных моделей:", reply_markup=reply_markup)

async def start(update, context):
    await update.message.reply_text("Для начала работы с ботом...")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Напиши команду /start чтобы начать генерацию сообщений")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    bot_name = query.data
    current_bot = Bot[bot_name]
    bot_readble_name = current_bot.value
    
    await query.answer()
    await query.edit_message_text(text=f"Вы выбрали бота: {bot_readble_name}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("bot", choose_model_menu))
    application.add_handler(CallbackQueryHandler(button))    

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_with_model_response))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()




















# bot = telebot.TeleBot(bot_token)


# def get_response(prompts):
#     res = requests.post(, json={"prompts": prompts})

# @bot.message_handler()
# def reply(message):
    
#     if message.text

#     model_output = 
#     reply = model_output['generated_text']
#     bot.reply_to(message, message.text)

# if __name__ == "__main__":
#     bot.infinity_polling()