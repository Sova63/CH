import telebot

TOKEN = '7066867801:AAHy3plobRxEskevJIjhxfHfM4bFkweuEj0'
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Привет! бот. Просто отправь мне запрос, и я найду информацию в Wikipedia для вас.")

bot.polling()