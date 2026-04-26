import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

WHATSAPP_LINK = "https://wa.me/77052304629"  # осы жерге өз WhatsApp номеріңді жаз


menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🚀 Бастау")],
        [KeyboardButton(text="📞 Байланыс")],
    ],
    resize_keyboard=True,
)

interest_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Иә, қызық")],
        [KeyboardButton(text="❌ Жоқ")],
    ],
    resize_keyboard=True,
)

age_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="18-25")],
        [KeyboardButton(text="26-35")],
        [KeyboardButton(text="36-45")],
        [KeyboardButton(text="45+")],
    ],
    resize_keyboard=True,
)

goal_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Қосымша табыс тапқым келеді")],
        [KeyboardButton(text="🏠 Үйден онлайн жұмыс істегім келеді")],
        [KeyboardButton(text="📈 Бизнес бастағым келеді")],
        [KeyboardButton(text="🤝 Командаға қосылғым келеді")],
        [KeyboardButton(text="ℹ️ Толығырақ білгім келеді")],
    ],
    resize_keyboard=True,
)

whatsapp_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📲 WhatsApp-қа жазу", url=WHATSAPP_LINK)]
    ]
)


class Form(StatesGroup):
    interest = State()
    name = State()
    age = State()
    goal = State()


async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Сәлем! 👋\n\n"
        "Мен Гүлжанның жеке көмекші ботымын.\n\n"
        "💰 Қазір көптеген адамдар онлайн табыс таба бастады.\n"
        "Сіз де сондай мүмкіндік іздеп жүрсіз бе?\n\n"
        "👇 Төмендегі батырманы басыңыз",
        reply_markup=menu_kb
    )


async def menu_start_handler(message: Message, state: FSMContext):
    await state.set_state(Form.interest)
    await message.answer(
        "Сіз қосымша табыс табу мүмкіндігін қарастырып жүрсіз бе? 💸",
        reply_markup=interest_kb,
    )


async def interest_handler(message: Message, state: FSMContext):
    text = message.text.strip()

    if text == "✅ Иә, қызық":
        await state.set_state(Form.name)
        await message.answer(
            "🔥 Керемет шешім!\n\n"
            "Қазір дұрыс ақпарат алсаңыз, жақсы нәтиже аласыз.\n\n"
            "Алдымен танысып алайық 👇\n"
            "Атыңыз кім?",
            reply_markup=ReplyKeyboardRemove(),
        )

    elif text == "❌ Жоқ":
        await state.clear()
        await message.answer(
            "Жақсы, шешіміңіз өзгерсе, қайта келіңіз 🌷",
            reply_markup=menu_kb,
        )

    else:
        await message.answer(
            "Төмендегі батырмалардың бірін таңдаңыз 👇",
            reply_markup=interest_kb,
        )


async def name_handler(message: Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await state.set_state(Form.age)

    await message.answer(
        f"{name}, қуаныштымын 🤝\n\n"
        "Жасыңыз қай аралықта?",
        reply_markup=age_kb,
    )


async def age_handler(message: Message, state: FSMContext):
    age = message.text.strip()
    allowed = ["18-25", "26-35", "36-45", "45+"]

    if age not in allowed:
    await message.answer("Төмендегі батырмалардың бірін таңдаңыз 👇", reply_markup=age_kb)
        return

    await state.update_data(age=age)
    await state.set_state(Form.goal)

    await message.answer(
        "Мақсатыңыз қандай?",
        reply_markup=goal_kb,
    )


async def goal_handler(message: Message, state: FSMContext):
    goal = message.text.strip()
    allowed_goals = [
        "💰 Қосымша табыс тапқым келеді",
        "🏠 Үйден онлайн жұмыс істегім келеді",
        "📈 Бизнес бастағым келеді",
        "🤝 Командаға қосылғым келеді",
        "ℹ️ Толығырақ білгім келеді",
    ]

    if goal not in allowed_goals:
    await message.answer("Төмендегі дайын жауаптардың бірін таңдаңыз 👇", reply_markup=goal_kb)
        return

    data = await state.get_data()
    name = data.get("name", "Белгісіз")
    age = data.get("age", "Белгісіз")
    username = message.from_user.username if message.from_user.username else "username жоқ"

    if ADMIN_ID:
    await message.bot.send_message(
         ADMIN_ID,
         "🔥 Жаңа лид!\n\n"
         f"👤 Аты: {name}\n"
         f"🎂 Жасы: {age}\n"
         f"🎯 Мақсаты: {goal}\n"
         f"📲 Telegram: @{username}",
     )

    await message.answer(
        "🔥 Сізге толық ақпарат дайын!\n\n"
        "⚡ Толық түсіндірме мен мысалдарды WhatsApp арқылы жібереміз.\n\n"
        "👇 WhatsApp арқылы жазыңыз 👇",
        reply_markup=ReplyKeyboardRemove(),
    )

    await message.answer(
        "📲 WhatsApp-қа өту үшін батырманы басыңыз:",
        reply_markup=whatsapp_button,
    )

    await state.clear()


async def contact_handler(message: Message):
    await message.answer(
        "⏳ Соңғы 24 сағатта бізге 17 адам жазды\n"
        "Сондықтан кешіктірмеңіз 👇\n\n"
        "📲 WhatsApp арқылы жазыңыз 👇",
        reply_markup=whatsapp_button,
    )


async def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN енгізілмеген")

    logging.basicConfig(level=logging.INFO)

    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, Command("start"))
    dp.message.register(menu_start_handler, F.text == "🚀 Бастау")
    dp.message.register(contact_handler, F.text == "📞 Байланыс")

    dp.message.register(interest_handler, Form.interest)
    dp.message.register(name_handler, Form.name)
    dp.message.register(age_handler, Form.age)
    dp.message.register(goal_handler, Form.goal)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
