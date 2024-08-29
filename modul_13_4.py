from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

from aiogram.types.base import Float

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
data = dict()
class UserState(StatesGroup):
    age = State()
    growth = State()
    weigth = State()

def m_cg_for_women():
    global data
    calories = (10*float(data['weigth']) + 6.25*float(data['growth']) -
                5*float(data['age']) - float(161))
    return calories
@dp.message_handler(text="Calories")
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message,state):
    global data
    await state.update_data(age= message.text)
    data = await state.get_data()
    #await state.finish()
    await message.answer('Введите свой рост в сантиметрах:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message,state):
    global data
    await state.update_data(growth= message.text)
    data = await state.get_data()
    #await state.finish()
    await message.answer('Введите свой вес:')
    await UserState.weigth.set()

@dp.message_handler(state=UserState.weigth)
async def set_weight(message,state):
    global data
    await state.update_data(weigth= message.text)
    data = await state.get_data()
    await state.finish()
    await  message.answer(f'Суточная норма калорий равна : {m_cg_for_women()}')




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)