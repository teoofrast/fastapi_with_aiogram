"""Модуль для запуска бота."""

# STDLIB
import asyncio

# THIRDPARTY
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
import httpx

# FIRSTPARTY
from tg_bot.settings.settings import BotSettings

bot_settings = BotSettings()
API_TOKEN = bot_settings.TG_BOT_TOKEN
FASTAPI_URL = bot_settings.FASTAPI_URL
BASE_NGROK_URL = bot_settings.BASE_NGROK_URL


bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: Message) -> None:
    """Обрабатывает команду /start.

    Эта функция вызывается, когда пользователь отправляет команду '/start'.
    Она отправляет информацию о пользователе на сервер FastAPI, чтобы
    зарегистрировать пользователя в системе, и в случае успеха отправляет
    приветственное сообщение.

    Аргументы:
        message (Message): Объект сообщения от пользователя, содержащий
        информацию о пользователе и его действиях.

    Описание:
        - Функция формирует словарь `payload` с данными пользователя.
        - Данные отправляются на сервер FastAPI для регистрации пользователя.
        - В случае ошибки при отправке запроса или получения ответа,
        пользователю будет отправлено сообщение с ошибкой.
        - После успешной регистрации пользователя, бот отправляет
        приветственное сообщение с именем и фамилией пользователя.

    Исключения:
        - httpx.RequestError: Ошибка при отправке HTTP-запроса.
        - httpx.HTTPStatusError: Ошибка при получении HTTP-ответа
        с неправильным статусом.
    """
    async with httpx.AsyncClient() as client:
        payload = {
            'id': message.from_user.id,
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
        }
        try:
            await client.post(f'{FASTAPI_URL}/api/v1/users', json=payload)
        except httpx.RequestError as e:
            await message.answer(f'Ошибка запроса: {e}')
            return
        except httpx.HTTPStatusError as e:
            await message.answer(f'Ошибка ответа: {e.response.status_code}')
            return

    await message.answer(
        f'Привет! {message.from_user.last_name} '
        f'{message.from_user.first_name} '
        'Добро пожаловать на мой бот.'
    )


@dp.message(Command('admin'))
async def send_admin(message: Message) -> None:
    """Отправляет пользователю клавиатуру.

    Эта функция вызывается при получении команды 'admin' от пользователя.
    Она формирует два URL для веб-приложений, которые предоставляют возможность
    управлять пользователями и услугами. Затем отправляется клавиатура с двумя
    кнопками: одной для управления пользователями и другой для управления
    услугами.

    Аргументы:
        message (Message): Объект сообщения от пользователя, содержащий
        информацию о пользователе и его запросах.
    """
    users_webapp_url = (
        f'{BASE_NGROK_URL}/api/v1/users?cur_user_id={message.from_user.id}'
    )
    services_webapp_url = (
        f'{BASE_NGROK_URL}/api/v1/services?cur_user_id={message.from_user.id}'
    )
    kb = [
        [
            KeyboardButton(
                text='Управление пользователями',
                web_app=WebAppInfo(url=users_webapp_url),
            )
        ],
        [
            KeyboardButton(
                text='Управление услугами',
                web_app=WebAppInfo(url=services_webapp_url),
            )
        ],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(
        'Снизу будет ссылка на админ-панель!', reply_markup=keyboard
    )


async def main() -> None:
    """Запускает основной цикл опроса для бота."""
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
