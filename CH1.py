import telebot
from telebot import types

bot = telebot.TeleBot('7066867801:AAHy3plobRxEskevJIjhxfHfM4bFkweuEj0')
habits = {}  # словарь для хранения привычек

# Декоратор для обработки команды старт
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я твой помощник для отслеживания привычек.\n"
                                      "Выбери действие:\n"
                                      "/view_stats - Просмотр статистики\n"
                                      "/add_habit - Добавить привычку\n"
                                      "/delete_habit - Удалить привычку\n"
                                      "/view_habits - Вывести список привычек")

# Обработка команды просмотра статистики
@bot.message_handler(commands=['view_stats'])
def view_stats(message):
    if not habits:
        bot.send_message(message.chat.id, "У тебя пока нет привычек.")
    else:
        stats = "\n".join([f"{name}: {data}" for name, data in habits.items()])
        bot.send_message(message.chat.id, f"Статистика привычек:\n{stats}")

# Обработка команды добавления привычки
@bot.message_handler(commands=['add_habit'])
def add_habit(message):
    bot.send_message(message.chat.id, "Введи название привычки:")
    bot.register_next_step_handler(message, add_habit_data)

def add_habit_data(message):
    habit_name = message.text
    habits[habit_name] = []
    bot.send_message(message.chat.id, f"Привычка '{habit_name}' добавлена. Введи данные (или /cancel для отмены):")
    bot.register_next_step_handler(message, add_habit_details, habit_name)

def add_habit_details(message, habit_name):
    if message.text == '/cancel':
        bot.send_message(message.chat.id, "Добавление привычки отменено.")
        return
    habits[habit_name].append(message.text)
    bot.send_message(message.chat.id, "Данные добавлены. Введи следующее (или /cancel для отмены):")
    bot.register_next_step_handler(message, add_habit_details, habit_name)

# Обработка команды удаления привычки
@bot.message_handler(commands=['delete_habit'])
def delete_habit(message):
    bot.send_message(message.chat.id, "Выбери привычку для удаления:")
    bot.register_next_step_handler(message, delete_habit_confirm)

def delete_habit_confirm(message):
    habit_name = message.text
    if habit_name in habits:
        del habits[habit_name]
        bot.send_message(message.chat.id, f"Привычка '{habit_name}' удалена.")
    else:
        bot.send_message(message.chat.id, "Такой привычки нет.")

# Обработка команды вывода списка привычек
@bot.message_handler(commands=['view_habits'])
def view_habits(message):
    if not habits:
        bot.send_message(message.chat.id, "У тебя пока нет привычек.")
    else:
        bot.send_message(message.chat.id, "Твои привычки:")
        for habit in habits:
            bot.send_message(message.chat.id, habit)

# Запуск бота
bot.polling(none_stop=True)
