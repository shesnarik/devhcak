from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatActions
from aiogram.types.web_app_info import WebAppInfo
import asyncio
from baza import Base, engine, db
from models import User

API = '6835397594:AAEE8QKEy8Yx0D-_HRXWGvNLMLDiAUN-V-U'

bot = Bot(API)
disp = Dispatcher(bot=bot)

# Сюда записываем ID пользователя, который админ 6128986459
admin_users_id = ['930661860']


@disp.message_handler(text='f')
async def edit(message: types.Message):
    await message.answer('dadas')
    user = db.query(User).filter(User.tg_user_id == message.from_user.id).first()
    if user is not None:
        user.sm_penis = 999
        db.commit()
    else:
        await message.answer('Юзер удалён')

# Подключаем базу данных
async def on_startap(_):
    Base.metadata.create_all(engine)
    print("База-Успешно!")


@disp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = User()
    user.tg_user_id = message.from_user.id
    user.sm_penis = 17
    db.add(user)
    db.commit()
    
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

        await message.answer(
            f"Режим администратора парковки:\n\n    User_name: @{message.from_user.username}\n    User_ID: {message.from_user.id}\n\nВыберите дествие: ", reply_markup=markup)
    else:
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        await asyncio.sleep(0.5)
        await message.answer(f"<b>Привет <i>@{message.from_user.username}</i></b> 🤚", parse_mode='html')
        await message.answer("Это платная парковка от Сбер\n\nЧтобы пользоваться парковкой нужно зарегистрироваться ✍️\n\n<b>Введите команду /contact</b>", parse_mode='html')

# Получение номера телефона
async def contact_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = types.KeyboardButton(text=("📱 Отправить"), request_contact=True)
    markup.add(first_button)
    return markup
@disp.message_handler(commands=("contact"))
async def share_number(message: types.Message):
    await message.answer("Нажмите на кнопку ниже, чтобы отправить номер телефона.", reply_markup=await contact_keyboard())
@disp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message):
    contact = message.contact
    await message.answer(f"Спасибо 😉\nВаш номер 📱 +{contact.phone_number} был получен.", reply_markup=types.ReplyKeyboardRemove())
        
@disp.message_handler(lambda message: message.text)
async def commands_button(message: types.Message):
    if message.text == 'Вывести данные 🗂️':
        
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text='Посмореть файл 🗂️', web_app=WebAppInfo(
            url='https://docs.google.com/document/d/1iectXmRwdJojmqtjC4vn7l19ecC5R_7brt863VfwMmo/edit'))
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

executor.start_polling(disp, on_startup=on_startap)
