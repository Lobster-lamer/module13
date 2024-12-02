from aiogram import Bot, Dispatcher,  types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import CommandStart
import constances
import asyncio



bot = Bot(token=constances.api)
dp = Dispatcher(storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@dp.message(F.text.lower().contains("калории"))
async def any_other_message(message: types.Message, state) -> None:
    await state.set_state(UserState.age)
    await message.answer("Введите свой возраст")

@dp.message(UserState.age)
async def set_growth(message: types.message, state) -> None:
    await state.update_data(age = message.text)
    await state.set_state(UserState.growth)
    await message.answer("Введите свой рост")

@dp.message(UserState.growth)
async def set_weight(message: types.message, state) -> None:
    await state.update_data(growth = message.text)
    await state.set_state(UserState.weight)
    await message.answer("Введите свой вес")

@dp.message(UserState.weight)
async def send_calories(message: types.message, state) -> None:
    await state.update_data(weight = message.text)
    data = await state.get_data()
    await message.answer(f"Ваша норма калорий: {get_female_norm_of_calories(data)}")
    await state.clear()

def get_male_norm_of_calories(data: dict) -> float:
    return 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5

def get_female_norm_of_calories(data: dict) -> float:
    return 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 161

@dp.message()
async def any_other_message(message: types.Message) -> None:
    await message.answer("Введите команду /start, чтобы начать общение.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())