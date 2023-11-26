import logging
from os import environ as env
from dotenv import load_dotenv

import telebot
import openai

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

load_dotenv()
bot = telebot.TeleBot(env["BOT_API_KEY"])
openai.api_key = env["OPENAI_API_KEY"]
user_id = int(env["USER_KEY"])


@bot.message_handler(func=lambda message: True)
def get_response(message):
  if int(message.chat.id) != user_id:
    bot.send_message("Этот бот предназначен для частного использования.")
  else:
    response = ""
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f'"""\n{message.text}\n"""',
    temperature=0.5,
    max_tokens=4000,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    stop=['"""'],
    )

    bot.send_message(message.chat.id, f'{response["choices"][0]["text"]}', parse_mode="None")

bot.infinity_polling()


