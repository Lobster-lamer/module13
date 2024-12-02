from aiogram import Bot, Dispatcher,  types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import CommandStart
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import constances
import asyncio


bot = Bot(token=constances.api)
dp = Dispatcher(storage=MemoryStorage())

kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Рассчитать"),KeyboardButton(text="Информация")]])
sex_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Мужчина"),KeyboardButton(text="Женщина")]],
                             one_time_keyboard=True)

inline_option_kb = InlineKeyboardMarkup(inline_keyboard=
                            [[InlineKeyboardButton(text="Рассчитать норму калорий",
                                                            callback_data="calories")],
                             [InlineKeyboardButton(text="Выбрать формулу расчёта",
                                                                 callback_data="formula")]])

inline_formula_kb = InlineKeyboardMarkup(inline_keyboard=
                            [[InlineKeyboardButton(text="Мужская: 10 * вес + 6.25 * рост - 5 * возраст + 5",
                                                            callback_data="male")],
                             [InlineKeyboardButton(text="Женская: 10 * вес + 6.25 * рост - 5 * возраст - 161",
                                                                 callback_data="female")]])


class UserState(StatesGroup):
    sex = State()
    age = State()
    growth = State()
    weight = State()
    options_answer_message: Message = None


@dp.message(CommandStart())
async def cmd_start(message: types.Message) -> None:
    await message.answer('Привет! Я бот помогающий твоему здоровью.',
                         reply_markup=kb)

@dp.message(F.text.lower().contains("рассчитать"))
async def options(message: types.Message, state) -> None:
    UserState.options_answer_message = message
    await state.set_state(UserState.sex)
    await message.answer("Выберите опцию:", reply_markup=inline_option_kb)


@dp.callback_query(F.data == "formula")
async def choose_formula(call) -> None:
    await call.message.answer("Выберите формулу:", reply_markup=inline_formula_kb)
    await call.message.delete()

@dp.callback_query(F.data == "male")
async def set_sex_to_male(call, state) -> None:
    await state.update_data(sex="Мужчина")
    await switch_to_options(call, state)

@dp.callback_query(F.data == "female")
async def set_sex_to_female(call, state) -> None:
    await state.update_data(sex="Женщина")
    await switch_to_options(call, state)

async def switch_to_options(call, state) -> None:
    await options(UserState.options_answer_message, state)
    await call.message.delete()

@dp.callback_query(F.data == "calories")
async def calories_solving_start(call, state) -> None:
    data = await state.get_data()
    if data.get("sex") is None:
        await state.update_data(sex="Мужчина")
    await state.set_state(UserState.age)
    await call.message.answer("Введите свой возраст", reply_markup=None)
    await call.message.delete()


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