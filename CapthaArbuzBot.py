import telebot
import random
import string
import json
import time
import re

characters = string.ascii_letters + string.digits

bot = telebot.TeleBot("6841246484:AAHD8SUxgu3Y6mqnSzcLuqFUQSltx8-PVr4", skip_pending=True)

def generate_captcha():
    captcha = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(9, 25)))
    return captcha
code = None

@bot.message_handler(commands=['id'])
def get_id(message):
    bot.reply_to(message, "Пришлите мне пересланное сообщение или отправьте своё")
    bot.register_next_step_handler(message, get_forwarded_message)
    
def get_forwarded_message(message):
    try:
        bot.reply_to(message, f"ID аккаунта этого сообщения:\n{message.forward_from.id}")
    except Exception as e:
        bot.reply_to(message, f"Не могу посмотреть ID этого аккаунта(")

@bot.message_handler(commands=['msg'])
def msg(message):
    match = re.match(r'\/msg "([^"]+)" "([^"]+)"', message.text)
    if match:
        id = match.group(1)
        text = match.group(2)
        first_name =  message.from_user.first_name
        last_name =  message.from_user.last_name
        last_name_str = last_name if last_name is not None else ""
        bot.send_message(int(id), f"Сообщение от <b>{first_name}</b> <b>{last_name_str}</b> : {text}", parse_mode="html")
        print(f'Сообщение от {first_name} {last_name_str} : {text}')

@bot.message_handler(commands=['Чек'])
def set(message):
    global code
    try:
        link = message.text.split(' ', 1)[1]
        code = ''.join(random.choice(characters) for _ in range(random.randint(13 , 45 )))
        bot.reply_to(message, f"https://t.me/SendChekArbuzBot?start={code}")
        if message.from_user.username:
            print(f"Создана ссылка для : {link}\nот [{message.from_user.id}|@{message.from_user.username}]")
        else:
            print(f"Создана ссылка для : {link}\nот [{message.from_user.id}]")
        text_code = ("/start " + code)
        with open("links.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
            data[f'{text_code}'] = link
            with open("links.json", 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False)
    except Exception as e:
        print(f"{message.from_user.id} : {message.from_user.id} \n{e}")

active_captchas = {}

def cap(message, data, txt):
    global code
    try:
        user_captcha = message.text
        correct_captcha = active_captchas.get(message.chat.id)
        if user_captcha == correct_captcha:
            if txt in data:
                bot.reply_to(message, data[txt])
            if message.from_user.username:
                inf = (f"Прошли капчу на : {data[txt]} : {message.from_user.id} : @{message.from_user.username}")
            else:
                inf = (f"Прошли капчу на : {data[txt]} : {message.from_user.id} : {message.from_user.id}")
            print(inf)
        else:
            bot.reply_to(message, f"капча для t.me/SendChekArbuzBot?start={code} была введена не верна!\nВот ваша капча которую вы вписали : <b>{user_captcha}</b>, а вот капча в боте <b>{correct_captcha}</b>", parse_mode="html")
            if message.from_user.username:
                inf = (f"Не прошли капчу на : {data[txt]} : {message.from_user.id} : @{message.from_user.username} | Капча бота : {correct_captcha}, Капча пользователя : {user_captcha}")
            else:
                inf = (f"Не прошли капчу на : {data[txt]} : {message.from_user.id} : {message.from_user.id} | Капча бота : {correct_captcha}, Капча пользователя : {user_captcha}")
            print(inf)
    except Exception as e:
        print("Ошибка при обработке капчи:", e)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Топовые раздачи тут -> \nhttps://t.me/+a-SE4OmY7g0wY2Q6")
    try:
        txt = message.text
        with open("links.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
            if txt in data:
                captcha = generate_captcha()
                bot.send_message(message.chat.id, text=f"""🤖Проверка на бота!
Нажмите на текст ниже ⤵️ (где ключи)
🔑<code>{captcha}</code>🔑
И отправьте скопированный текст боту в новом сообщении.
У вас 1 попытка!""", parse_mode="html")
                active_captchas[message.chat.id] = captcha
                bot.register_next_step_handler(message, lambda msg: cap(msg, data, txt))
        file.close()
    except Exception as e:
        print(f"{message.from_user.id} : {message.from_user.id} \n{e}")
        
def main_polling():
    while True:
        try:
            bot.polling(non_stop=True)
        except Exception as e:
            print("Error occurred:", e)
            time.sleep(1)

if __name__ == "__main__":
    main_polling()
