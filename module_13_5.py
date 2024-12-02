from aiogram import Bot, Dispatcher,  types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import constances
import asyncio



bot = Bot(token=constances.api)
dp = Dispatcher(storage=MemoryStorage())

kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Рассчитать"),KeyboardButton(text="Информация")]])
sex_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Мужчина"),KeyboardButton(text="Женщина")]],
                             one_time_keyboard=True)


class UserState(StatesGroup):
    sex = State()
    age = State()
    growth = State()
    weight = State()


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer('Привет! Я бот помогающий твоему здоровью.',
                         reply_markup=kb)

@dp.message(F.text.lower().contains("рассчитать"))
async def set_sex(message: types.Message, state) -> None:
    await state.set_state(UserState.sex)
    await message.answer("Выберите свой пол", reply_markup=sex_kb)

@dp.message(UserState.sex)
async def set_age(message: types.Message, state) -> None:
    await state.update_data(sex=message.text)
    await state.set_state(UserState.age)
    await message.answer("Введите свой возраст", reply_markup=None)

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
    await message.answer(f"Ваша норма калорий: {get_norm_of_calories(data)}",
                         reply_markup=kb)
    await state.clear()

def get_norm_of_calories(data: dict) -> float:
    if data["sex"] == "Мужчина":
        return 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
    elif data["sex"] == "Женщина":
        return 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 161
    else:
        return "Не совсем понятен ваш пол"

@dp.message()
async def any_other_message(message: types.Message) -> None:
    await message.answer("Введите команду /start, чтобы начать общение.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())