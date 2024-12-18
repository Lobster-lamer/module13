from aiogram import Bot, Dispatcher,  types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters.command import Command
import constances
import asyncio


bot = Bot(token=constances.api)
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message()
async def any_other_message(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())