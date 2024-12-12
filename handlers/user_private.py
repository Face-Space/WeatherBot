from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f, StateFilter
import requests
import json
import os
import asyncio


from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from translate import Translator
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

from FSM import UserSelect

from database.orm_query import orm_add_user, orm_get_user, orm_delete_user
from keyboards import reply
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

API = os.getenv('API')
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
translator = Translator(from_lang='english', to_lang='russian')
user_private_router = Router()


async def get_weather(message: types.Message, city, state: FSMContext):
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    if res.status_code == 200:
        UserSelect.continuation = True
        data = json.loads(res.text)
        weather = translator.translate(data["weather"][0]["main"])
        await message.answer(f'🌃В городе {city} сейчас: {weather}')
        await asyncio.sleep(2)
        await message.answer(f'🌡Температура {data["main"]["temp"]}, но ощущается🥶 как {data["main"]["feels_like"]}')
        await asyncio.sleep(2)
        await message.answer(f'🪁Атмосферное давление {data["main"]["pressure"]} мм рт')
        await asyncio.sleep(2)
        await message.answer(f'💧Влажность воздуха {data["main"]["humidity"]}%')
        await asyncio.sleep(3)
        await message.answer("Для быстрого доступа к погоде🌤, можете сразу написать здесь нужный Вам город🌆 "
                             "или скинуть свою геопозицию📍, чтобы узнать погоду в вашем районе", reply_markup=reply.start_kb)
    else:
        await message.answer("Извините, но указан неверный город😔, попробуйте еще раз", reply_markup=reply.start_kb)
        await state.clear()
        UserSelect.my_user = None
        UserSelect.continuation = False

@user_private_router.message(or_f(CommandStart(), F.text.lower().contains("перезапуск")))
async def start_cmd(message: types.Message, state: FSMContext):
    await message.answer("Доброго времени суток!👋 Этот бот🤖 поможет узнать погоду в любой точке мира!🌍 \n"
                         "Пожалуйста, укажите интересующий вас город🏙", reply_markup=reply.start_kb)
    await state.clear()


@user_private_router.message(or_f(Command("location"), F.text.lower().contains("гео")))
async def permission_loc(message: types.Message, state: FSMContext):
    await message.answer("Нажмите кнопку📌 'Отправить свою геопозицию'📍 чуть ниже👇",
                         reply_markup=reply.start_kb)
    await state.clear()


@user_private_router.message(or_f(Command("notifications"), F.text.lower().contains("уведом")))
async def note_cmd(message: types.Message, session: AsyncSession, state: FSMContext):

    if UserSelect.my_user is None:
        await message.answer("Напишите город🌆, погоду которого вы хотите получать каждую минуту🕓")
        # UserSelect.my_user = orm_get_user(session, message.from_user.id)
        await state.set_state(UserSelect.city)

    elif UserSelect.my_user == 'cancel_enable':
        await orm_delete_user(session, message.from_user.id)
        scheduler.remove_job('get_weather_job')
        scheduler.shutdown()
        await message.answer("❌Уведомления отключены❌", reply_markup=reply.start_kb)
        UserSelect.my_user = None
        await state.clear()


@user_private_router.message(UserSelect.city, F.text)
async def mini_server(message: types.Message, session: AsyncSession, state: FSMContext):

    city = message.text.strip()

    try:
        if UserSelect.my_user is None:
            await orm_add_user(message, session)
            UserSelect.my_user = 'cancel_enable'

        await get_weather(message, city, state)

        if UserSelect.continuation:
            scheduler.add_job(get_weather, trigger='interval', minutes=1,
                              kwargs={'message': message, 'city': city, 'state': state}, id='get_weather_job')
            scheduler.start()
            await message.answer(f"Уведомления включены🔔. Теперь состояние погоды☀️ в городе {city} будет "
                                 "присылаться вам раз в <b>1</b> мин⏱️")
            await asyncio.sleep(1)
            await message.answer("Чтобы отключить уведомления🔕 нажмите "
                                 "/notifications или кнопку 'Уведомления' внизу👇", reply_markup=reply.start_kb)
            UserSelect.continuation = None
            await state.clear()

    except requests.exceptions.ReadTimeout:
        await message.answer("Извините, произошла ошибка😕, попробуйте ещё раз")

    except requests.exceptions.ConnectTimeout:
        await message.answer("Извините, сервер перегружен😕, попробуйте позже")


    # scheduler.add_job(exp, trigger='date', run_date=datetime.now() + timedelta(seconds=10),
    #                   kwargs={'message': message})
    # scheduler.add_job(exp, trigger='cron', hour=datetime.now().hour, minute=datetime.now().minute + 1,
    #                   start_date=datetime.now(), kwargs={'message': message})

@user_private_router.message(F.location)
async def get_location(message: types.Message, state: FSMContext):
    lat = str(message.location.latitude)
    lon = str(message.location.longitude)
    res = requests.get(f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API}")
    data = json.loads(res.text)
    city = data[0]["local_names"]["ru"]
    await get_weather(message, city, state)


@user_private_router.message(F.text)
async def today_weather(message: types.Message, state: FSMContext):
    city = message.text.strip()
    await get_weather(message, city, state)


@user_private_router.message()
async def idk(message: types.Message):
    await message.answer("Извините, я Вас не понимаю😔, напишите пожалуйста нужный Вам город")




