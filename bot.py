import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# 🔑 ENV
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# 🔘 МЕНЮ
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Бастау")],
        [KeyboardButton(text="📞 Байланыс")]
    ],
    resize_keyboard=True
)

# 📲 WHATSAPP КНОПКА
whatsapp_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="📲 WhatsApp жазу",
            url="https://wa.me/77052304629"  # ⚠️ ОСЫ ЖЕРГЕ ӨЗ НОМЕРІҢДІ ЖАЗ
        )]
    ]
)

# 📊 СТЕЙТТЕР
class Form(StatesGroup):
    name = State()
    age = State()
    goal = State()


# 🚀 /start
async def start_handler(message: Message):
    await message.answer(
        "Сәлем! 👋\n\nБіз сізге көмектесеміз.\n\nБастау үшін батырманы бас:",
        reply_markup=menu
    )


# 🚀 БАСТАУ БАТЫРМАСЫ
async def start_flow(message: Message, state: FSMContext):
    await message.answer("1️⃣ Сіздің атыңыз?")
    await state.set_state(Form.name)


# 1️⃣ АТЫ
async def q1(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("2️⃣ Жасыңыз қанша?")
    await state.set_state(Form.age)


# 2️⃣ ЖАСЫ
async def q2(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("3️⃣ Мақсатыңыз қандай?")
    await state.set_state(Form.goal)


# 3️⃣ МАҚСАТ + ФИНАЛ
async def q3(message: Message, state: FSMContext):
    data = await state.get_data()

    name = data["name"]
    age = data["age"]
    goal = message.text

    # 🔥 АДМИНГЕ ЖІБЕРУ
    await message.bot.send_message(
        ADMIN_ID,
        f"🔥 Жаңа лид:\n\n"
        f"👤 Аты: {name}\n"
        f"🎂 Жасы: {age}\n"
        f"🎯 Мақсаты: {goal}"
    )

    # 👤 КЛИЕНТКЕ ЖАУАП
    await message.answer(
        "🔥 Рахмет! Біз сізбен байланысамыз.\n\n"
        "📲 Қазір WhatsApp-қа жазыңыз:",
        reply_markup=whatsapp_button
    )

    await state.clear()


# 📞 БАЙЛАНЫС
async def contact_handler(message: Message):
    await message.answer(
        "📲 Бізге жазыңыз:",
        reply_markup=whatsapp_button
    )


# 🔧 MAIN
async def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN енгізілмеген")

    logging.basicConfig(level=logging.INFO)

    bot = Bot(TOKEN)
    dp = Dispatcher()

    # РЕГИСТРАЦИЯ
    dp.message.register(start_handler, Command("start"))
    dp.message.register(start_flow, F.text == "🚀 Бастау")
    dp.message.register(contact_handler, F.text == "📞 Байланыс")

    dp.message.register(q1, Form.name)
    dp.message.register(q2, Form.age)
    dp.message.register(q3, Form.goal)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
