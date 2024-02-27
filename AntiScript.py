import telebot
import random
import string
import json

characters = string.ascii_letters + string.digits

# Создаем экземпляр бота
bot = telebot.TeleBot("6459219591:AAHts-0Uv-PnehQoto0fbdVEZGnKVwZ75bc", skip_pending=True)

# Функция для генерации случайной капчи
def generate_captcha():
    captcha = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(9, 20)))
    return captcha

@bot.message_handler(commands=['Чек'])
def set(message):
    try:
        link = message.text.split(' ', 1)[1]
        code = ''.join(random.choice(characters) for _ in range(random.randint(13, 30)))
        bot.reply_to(message, f"https://t.me/ScriptScanBot_bot?start={code}")
        if message.from_user.username:
            print(f"Создаена ссылка для : {link}\nот [{message.from_user.id}|@{message.from_user.username}]")
        else:
            print(f"Создаена ссылка для : {link}\nот [{message.from_user.id}]")
        text_code = ("/start " + code)
        with open("captha.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
            data[f'{text_code}'] = link
            with open("captha.json", 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False)
    except Exception as e:
        print(f"{message.from_user.id} : {message.from_user.id} \n{e}")

active_captchas = {}

def cap(message, data, txt):
    try:
        # Получаем введенную пользователем капчу
        user_captcha = message.text
        # Получаем капчу, сгенерированную ранее для данного пользователя
        correct_captcha = active_captchas.get(message.chat.id)
        
        # Проверяем, соответствует ли введенная капча правильной
        if user_captcha == correct_captcha:
            if txt in data:
                bot.reply_to(message, data[txt])
            if message.from_user.username:
                inf = (f"{data[txt]} : {message.from_user.id} : @{message.from_user.username}")
            else:
                inf = (f"{data[txt]} : {message.from_user.id} : {message.from_user.id}")
            print(inf)
    except Exception as e:
        print("Ошибка при обработке капчи:", e)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Самые большие раздачи арбузов тут -> \nhttps://t.me/+_8Qa55e-7TExYTdl")
    try:
        txt = message.text
        with open("captha.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
            if txt in data:
                captcha = generate_captcha()  # Функция generate_captcha() должна быть определена где-то в вашем коде
                bot.send_message(message.chat.id, f"Введите последовательность символов из этой капчи: {captcha}")
                active_captchas[message.chat.id] = captcha
                bot.register_next_step_handler(message, lambda msg: cap(msg, data, txt))
        file.close()
    except Exception as e:
        print(f"{message.from_user.id} : {message.from_user.id} \n{e}")
        
bot.polling(non_stop=True)