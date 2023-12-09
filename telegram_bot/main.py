import os
from enum import Enum

import requests
from telegram.ext import CommandHandler, CallbackQueryHandler, Application, ContextTypes, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

class Bot(Enum):
    VOLK='Волк'
    PUSHKIN='Пушкин'

TEXT_GENERATOR_URL='http://text_generator_container:5001'
GENERATE_TEXT_URL=TEXT_GENERATOR_URL + "/generate"
CHANGE_MODEL_URL=TEXT_GENERATOR_URL + "/change_model"
TG_TOKEN_PATH = os.getenv('TG_TOKEN')
with open(TG_TOKEN_PATH, "r") as file:
    TG_TOKEN = file.readline()


async def reply_with_model_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt=update.message.text
    user=update.message.from_user
    json_request= {
        "prompts": prompt,
        "user": {
            "id": user["id"],
            "username": user["username"]
        }
    }
    print(json_request)
    json_reply = requests.post(GENERATE_TEXT_URL, json=json_request).json()
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
    
    # print user data
    # print(update)
    #
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
    requests.post(CHANGE_MODEL_URL, json=json_request)
    
    # Print user's choice
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
