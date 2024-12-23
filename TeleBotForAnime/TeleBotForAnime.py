import telebot
from telebot import types
from config import BOT_TOKEN
from database import blue_lock_2nd_season

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🎥 Найти аниме-серию")
    btn2 = types.KeyboardButton("⚽ Blue Lock 2 сезон: Блю Лок против юношеской сборной Японии")
    markup.add(btn1, btn2)
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я помогу тебе найти серии аниме. Нажми на кнопку ниже, чтобы начать!",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "🎥 Найти аниме-серию":
        bot.send_message(message.chat.id, "Введите название аниме:")
    elif message.text == "⚽ Blue Lock 2 сезон: Блю Лок против юношеской сборной Японии":
        select_episode(message.chat.id)
    elif message.text in blue_lock_2nd_season:
        send_episode_link(message)
    else:
        bot.send_message(message.chat.id, "❌ Команда не распознана. Попробуйте снова.")

def select_episode(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for episode in blue_lock_2nd_season.keys():
        markup.add(types.KeyboardButton(episode))
    bot.send_message(
        chat_id,
        "Выберите серию из второго сезона Blue Lock:",
        reply_markup=markup
    )

def send_episode_link(message):
    video_url = blue_lock_2nd_season[message.text]
    bot.send_message(message.chat.id, f"🔗 Ссылка на {message.text}: {video_url}")

bot.polling(none_stop=True)
