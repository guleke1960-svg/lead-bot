import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
TEST_BOT_LINK = os.getenv("TEST_BOT_LINK", "https://t.me/your_test_bot")


class LeadState(StatesGroup):
    waiting_interest = State()
    waiting_name = State()


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Иә, қызық")],
        [KeyboardButton(text="❌ Жоқ")],
    ],
    resize_keyboard=True,
)


async def start_handler(message: Message, state: FSMContext):
    await state.set_state(LeadState.waiting_interest)
    await message.answer(
        "Сәлем 👋\n\n"
        "Мен Гүлжанның жеке көмекші ботымын.\n\n"
        "Сіз қосымша табыс табу мүмкіндігін қарастырып жүрсіз бе? 💸\n\n"
        "Қысқа тесттен өтіп, сізге ең тиімді бағытты анықтап берейін 👇",
        reply_markup=main_kb,
    )


async def interest_handler(message: Message, state: FSMContext):
    text = message.text.strip()

    if text == "✅ Иә, қызық":
        await state.set_state(LeadState.waiting_name)
        await message.answer("Керемет 👍\n\nАлдымен танысып алайық 😊\nАтыңыз кім?")

    elif text == "❌ Жоқ":
        await message.answer("Жақсы, шешіміңіз өзгерсе, қайта жазыңыз 🌷")

    else:
        await message.answer("Төмендегі батырмалардың бірін таңдаңыз 👇")


async def name_handler(message: Message, state: FSMContext):
    name = message.text.strip()

    await state.update_data(name=name)

    if ADMIN_ID:
        await message.bot.send_message(
            ADMIN_ID,
            f"🔥 Жаңа лид!\n\nАты: {name}\nUsername: @{message.from_user.username if message.from_user.username else 'жоқ'}"
        )

    await message.answer(
        f"{name}, қуаныштымын 🤝\n\n"
        "Сізге дұрыс ұсыныс беру үшін 1-2 сұрақ қоямын 👇\n\n"
        f"Тест ботқа өту үшін осы сілтемені ашыңыз: {TEST_BOT_LINK}"
    )

    await state.clear()


async def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN енгізілмеген")
    if not ADMIN_ID:
        logging.warning("ADMIN_ID енгізілмеген")

    logging.basicConfig(level=logging.INFO)

    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.message.register(start_handler, CommandStart())
    dp.message.register(interest_handler, StateFilter(LeadState.waiting_interest))
    dp.message.register(name_handler, StateFilter(LeadState.waiting_name))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
