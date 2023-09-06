import pandas
import json
import telebot
import subprocess

#users = [868124242, 000000000]
token = '6467012974:AAE6_XU_jQvcuE9_4Q_jDAZ3MikfgS5bgBg'
bot = telebot.TeleBot(token)

data = pandas.read_excel('data.xlsx')
date = list(map(str, data['date']))
nikName = list(map(str.lower, data['nik']))
gold = list(data['gold'])
damage = list(data['damage'])
hero = list(data['hero'])
koof = list(round(data['koof'], 2))

#Обрезаем лишние симфолы в дате
modyffed_date =[]
for index in date:
    modyffed_date.append(index.rstrip(' 00:00:00'))

# Читаем белый список для дальнейшего сравнения есть ли пользователь в нем
with open("white_list", "r") as vrem_file:
    spisok_id = vrem_file.read()

@bot.message_handler(commands=['start'])
def check_and_write_number(number):
    # Открываем файл в режиме чтения
    with open("white_list", "r") as file:
        # Читаем содержимое файла и проверяем наличие числа
        existing_numbers = file.read().split()
        if str(number.from_user.id) in existing_numbers:
            print("Число уже есть в файле")
            return

    # Открываем файл в режиме добавления (если файла нет, он будет создан)
    with open("white_list", "a") as file:
        # Записываем число в файл
        file.write(str(number.from_user.id) + "\n")
        print("Число успешно добавлено в файл")

@bot.message_handler(commands=['nik'])
def info_user(message):
    user_id = str(message.from_user.id)
    if user_id in spisok_id:
        bot.send_message(message.chat.id, 'Введите Nik игрока:')
        bot.register_next_step_handler(message, nik_info)
    else:
        bot.reply_to(message, "Вы не имеете доступа к этой команде.")
def upload_nik_info(nik):
    allParam = []
    for index in range(len(nikName)):
        if nikName[index] == nik:
            allParam.append(modyffed_date[index])
            allParam.append(hero[index])
            allParam.append(damage[index])
            allParam.append(koof[index])

    with open("res.json", "w") as file:
        json.dump(allParam, file, indent=4, ensure_ascii=False)
        allParam = []
def nik_info(message):
    text = message.text.lower()
    if text in nikName:
        upload_nik_info(text)
        with open('res.json') as jf:
            infa_json = json.load(jf)
            bot.send_message(message.chat.id, f'<b>{text}</b> \n '
                                              f'<b>Дата                Герой   Урон    Коэф.</b>\n'
                                              f'{infa_json}', parse_mode='HTML')

    else:
        bot.send_message(message.chat.id, f'Игрок с ником - {text} не играл в Гильдии Рич, если вы уверены в обратном попробуйте написать ник по другому')

@bot.message_handler(commands=["restart"]) #вызов по команде /restart; можно сделать и на кнопку
def restart(message):
    status = subprocess.check_output("sudo systemctl restart mybot.service", shell=True)


bot.polling()

