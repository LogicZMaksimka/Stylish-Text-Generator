import os
from enum import Enum

import requests
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

class Bot(Enum):
    VOLK='Волк'
    PUSHKIN='Пушкин'

REQUEST_TIMEOUT=5
TEXT_GENERATOR_URL=os.getenv("TEXT_GENERATOR_URL")
GENERATE_TEXT_URL=TEXT_GENERATOR_URL + "/generate"
CHANGE_MODEL_URL=TEXT_GENERATOR_URL + "/change_model"

TG_TOKEN_PATH = os.getenv('TG_TOKEN')
with open(TG_TOKEN_PATH, "r", encoding='UTF-8') as file:
    TG_TOKEN = file.readline()


async def reply_with_model_response(update: Update):
    prompt=update.message.text
    user=update.message.from_user
    json_request= {
        "prompts": prompt,
        "user": {
            "id": user["id"],
            "username": user["username"]
        }
    }
    reply = requests.post(GENERATE_TEXT_URL, json=json_request, timeout=REQUEST_TIMEOUT)
    if reply is None:
        return
    json_reply = reply.json()
    generated_text = json_reply[0]["generated_text"]
    await update.message.reply_text(generated_text)

async def choose_model_menu(update: Update):
    keyboard = [
        [InlineKeyboardButton('Бот Bолк', callback_data=Bot.VOLK.name)],
        [InlineKeyboardButton('Бот Пушкин', callback_data=Bot.PUSHKIN.name)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Выберите одну из доступных моделей:", reply_markup=reply_markup)

async def start(update: Update):
    welcome_message = """

    Здравствуй пользователь\! 
    
    Этот бот генерирует продолжения ваших сообщений в различных стилях\. На данный момент поддерживаются 2 модели\:
    \- Бот Волк \- обучался на мемах с "волчьими цитатами"
    \- Бот Пушкин \- обучался на собрании стихов Пушкина

    Для смены бота используйте команду /bot
    """
    await update.message.reply_text(welcome_message)
    await choose_model_menu(update)

async def help_command(update: Update):
    await update.message.reply_text("Для смены бота используйте команду /bot")

async def button(update: Update):
    query = update.callback_query
    
    # Update model for specific user
    user = query.from_user
    bot_name = query.data
    json_request = {
        "bot": bot_name,
        "user": {
            "id": user["id"],
            "username": user["username"]
        }
    }
    requests.post(CHANGE_MODEL_URL, json=json_request, timeout=REQUEST_TIMEOUT)
    
    # Response with user's choice
    bot_readble_name = Bot[bot_name].value
    await query.answer()
    await query.edit_message_text(text=f"Вы выбрали бота: {bot_readble_name}")

def main():
    application = Application.builder().token(TG_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("bot", choose_model_menu))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_with_model_response))
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
