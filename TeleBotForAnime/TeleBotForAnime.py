import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot('BOT-TOKEN')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🎥 Найти аниме-серию")
    markup.add(btn1)
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я помогу тебе найти серии аниме. Нажми на кнопку ниже, чтобы начать!",
        reply_markup=markup
    )

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "🎥 Найти аниме-серию":
        bot.send_message(message.chat.id, "Введите название аниме:")
    else:
        search_anime(message.text, message.chat.id)

def search_anime(query, chat_id):
    url = f"https://gogoanime.tel//search.html?keyword={query.replace(' ', '%20')}"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        results = soup.find_all('p', class_='name')
        if not results:
            bot.send_message(chat_id, "❌ Аниме не найдено. Попробуйте другое название.")
            return

        message = "📜 Вот что я нашёл:\n\n"
        for result in results[:5]:
            title = result.a.text
            link = "https://gogoanime.tel" + result.a['href']
            message += f"🔗 [{title}]({link})\n"

        bot.send_message(chat_id, message, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(chat_id, "⚠ Произошла ошибка. Попробуйте позже.")
        print(e)

bot.polling(none_stop=True)
