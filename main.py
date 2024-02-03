import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatActions
from aiogram.types.web_app_info import WebAppInfo
import asyncio
import sqlite3
import baza as db

API = '6835397594:AAEE8QKEy8Yx0D-_HRXWGvNLMLDiAUN-V-U'

bot = Bot(API)
disp = Dispatcher(bot=bot)

# Сюда записываем ID пользователя, который админ
admin_users_id = ['6128986459']

# Подключаем базу данных
async def on_startap(_):
    await db.db_baze()
    print("База-Успешно!")

@disp.message_handler(commands=['start'])
async def start(message: types.Message):
    if str(message.from_user.id) in admin_users_id:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton(text='Вывести данные 🗂️')
        btn2 = types.KeyboardButton(text='Добавить авто 🚘')
        btn3 = types.KeyboardButton(text='Редактировать водителя 💳')
        btn4 = types.KeyboardButton(text='Задать время 🧭')
        btn5 = types.KeyboardButton(text='Удалить авто 🚗')
        
        markup.row(btn1, btn2)
        markup.add(btn3)
        markup.row(btn4, btn5)
        
        await message.answer(f"Режим администратора парковки:\n\n    User_name: @{message.from_user.username}\n    User_ID: {message.from_user.id}\n\nВыберите дествие: ", reply_markup=markup)
    else:
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(0.5)
        await message.answer(f"<b>Привет <i>@{message.from_user.username}</i></b> 🤚", parse_mode='html')

@disp.message_handler(lambda message: message.text)
async def commands_button(message: types.Message):
    if message.text == 'Вывести данные 🗂️':
        
        with open('https://docs.google.com/document/d/1iectXmRwdJojmqtjC4vn7l19ecC5R_7brt863VfwMmo/edit') as file:
            file.write("Hello")
        
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Посмореть файл 🗂️', web_app=WebAppInfo(url='https://docs.google.com/document/d/1iectXmRwdJojmqtjC4vn7l19ecC5R_7brt863VfwMmo/edit'))
        markup.add(btn1)
        
        await message.answer("Список автомобилей, сотрудников УК", reply_markup=markup)
        
    elif message.text == 'Добавить авто 🚘':
        await message.answer("Введите ГОС номер автомобиля: ")
    elif message.text == 'Редактировать водителя 💳':
        await message.answer("Выберите какого водиеля изменить данные: ")
    elif message.text == 'Задать время 🧭':
        await message.answer("Задайте время парковки автомобиля: ")
    elif message.text == 'Удалить авто 🚗':
        await message.answer("Введите ГОС номер автомобиля: ")

executor.start_polling(disp, skip_updates=True, on_startup=on_startap)
