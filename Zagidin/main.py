from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import sqlite3

API = '6835397594:AAEE8QKEy8Yx0D-_HRXWGvNLMLDiAUN-V-U'
storage = MemoryStorage()
bot = Bot(API)
disp = Dispatcher(bot=bot, storage=storage)

class Registration(StatesGroup):
    WaitingForName = State()
    WaitingForLastName = State()
    WaitingForOtchestvo = State()
    WaitingForPhoneNumber = State()

@disp.message_handler(commands=["start"])
async def start(message: types.Message, state: FSMContext):
    # Сброс состояния FSM
    await state.finish()
    await message.answer(f"Привет @{message.from_user.username} 🤚\n\nДавайте для начала вас зарегистрируем ✍️")
    await message.answer("Как к Вам обращаться? ")
    await Registration.WaitingForName.set()

# Получаем имя, фамилие, отчество, номер телефона
@disp.message_handler(state=Registration.WaitingForName)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Теперь введите свою фамилию")
    await Registration.WaitingForLastName.set()

@disp.message_handler(state=Registration.WaitingForLastName)
async def process_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text
    await message.answer("Отлично! Введите отчество")
    await Registration.WaitingForOtchestvo.set()
    
@disp.message_handler(state=Registration.WaitingForOtchestvo)
async def process_otchestvo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['otchestvo'] = message.text
    await message.answer("Супер! Теперь осталось ввести номер телефона")
    await Registration.WaitingForPhoneNumber.set()

@disp.message_handler(state=Registration.WaitingForPhoneNumber)
async def process_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
        
        # Сохраняем в базу данных
        save_to_database(data['name'], data['last_name'], data['otchestvo'], data['phone_number'])
    await message.answer("Спасибо! Регистрация завершена 📋")

# Сохранение данных в базу данных
def save_to_database(name, last_name, otchestvo, phone_number):
    db = sqlite3.connect('parkovka.db')
    cursor = db.cursor()
    cursor.execute("INSERT INTO parking (Имя, Фамилие, Отчество, Номер_телефона) VALUES (?, ?, ?, ?)", (name, last_name, otchestvo, phone_number))
    db.commit()
    db.close()
    
executor.start_polling(disp)