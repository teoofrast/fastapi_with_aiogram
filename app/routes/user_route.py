"""Маршруты для управления пользователями."""

# STDLIB
from http import HTTPStatus

# THIRDPARTY
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse, RedirectResponse

# FIRSTPARTY
from app.DAL.BaseDAL import UserDAL
from app.database import SessionDep
from app.schemas.schemas import UserCreateSchema
from tg_bot.settings.settings import BotSettings

router = APIRouter()

templates = Jinja2Templates(directory='templates')

bot_settings = BotSettings()


@router.post('/api/v1/users')
async def add_user(user: UserCreateSchema, session: SessionDep) -> dict:
    """Добавляет нового пользователя.

    Эта функция обрабатывает POST-запрос на создание нового пользователя.
    Если пользователь с данным ID уже существует, возвращается сообщение
    о том, что пользователь уже зарегистрирован. В случае успешной регистрации
    возвращаются данные нового пользователя.

    Параметры:
        user (UserCreateSchema): Схема данных для создания нового пользователя.
        session (SessionDep): Сессия базы данных для выполнения операций.

    Возвращаемое значение:
        dict: Возвращает словарь с статусом, сообщением и данными пользователя:
            - Если пользователь был успешно добавлен, возвращает статус 200
              и данные нового пользователя.
            - Если пользователь с таким ID уже существует, возвращает статус
            400 и данные существующего пользователя.
    """
    cur_user = await UserDAL.get_by_id(user.id, session)
    if cur_user is None:
        new_user = await UserDAL.add_one_user(user, session)
        return {
            'status': 200,
            'message': 'Поздравляю с регистрацией',
            'id': new_user.id,
            'username': new_user.username,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
        }
    else:
        return {
            'status': 400,
            'message': 'Пользователь уже зарегистрирован',
            'id': cur_user.id,
            'username': cur_user.username,
            'first_name': cur_user.first_name,
            'last_name': cur_user.last_name,
        }


@router.get('/api/v1/users')
async def get_users(request: Request, session: SessionDep, cur_user_id: int):
    """Получает список пользователей для администраторов.

    Эта функция обрабатывает GET-запрос для получения списка всех юзеров.
    Доступ к списку имеют только пользователи с правами администратора. Если
    текущий пользователь не является администратором, возвращается сообщение
    о запрете доступа.

    Параметры:
        request (Request): Объект запроса, передаваемый в шаблон.
        session (SessionDep): Сессия базы данных для выполнения запросов.
        cur_user_id (int): ID текущего пользователя, выполняющего запрос.

    Возвращаемое значение:
        Union[TemplateResponse, JSONResponse]:
            Если текущий пользователь является администратором, возвращается
            HTML-шаблон с данными пользователей. Иначе возвращается
            JSON-ответ с сообщением о запрете доступа.
    """
    user = await UserDAL.get_by_id(cur_user_id, session)
    if user:
        if user.is_admin:
            users = await UserDAL.get_all(session)
            return templates.TemplateResponse(
                'index.html',
                {
                    'request': request,
                    'title': 'Пользователи',
                    'users': users,
                    'cur_user_id': cur_user_id,
                },
            )
    else:
        return JSONResponse(
            content={'message': 'Access denied'},
            status_code=HTTPStatus.UNAUTHORIZED,
        )


@router.get('/api/v1/users/edit/{user_id}')
async def edit_user(
    request: Request, user_id: int, session: SessionDep, cur_user_id: int
):
    """Обрабатывает запрос для редактирования информации о пользователе.

    Эта функция обрабатывает GET-запрос на редактирование данных пользователя.
    Она извлекает пользователя из базы данных по его ID и возвращает страницу
    для редактирования с данными о пользователе, если он найден.

    Параметры:
        request (Request): Объект запроса для передачи в шаблон.
        user_id (int): ID юзера, информацию которого нужно отредактировать.
        session (SessionDep): Сессия базы данных для выполнения запросов.
        cur_user_id (int): ID текущего юзера, который выполняет операцию.

    Возвращаемое значение:
        TemplateResponse: Отправляет HTML-шаблон с данными для редактирования.
    """
    user = await UserDAL.get_by_id(user_id, session)
    if user:
        return templates.TemplateResponse(
            'edit_user.html',
            {
                'request': request,
                'title': 'Редактирование пользователя',
                'user': user,
                'cur_user_id': cur_user_id,
            },
        )


@router.post('/api/v1/users/update/{user_id}')
async def update_user(
    request: Request,
    session: SessionDep,
    user_id: int,
    cur_user_id: int,
    username: str = Form(...),
    user_firstname: str = Form(...),
    user_lastname: str = Form(...),
    is_admin: bool = Form(...),
):
    """Обновляет информацию о пользователе и возвращает редирект или ошибку.

    Параметры:
        request (Request): Объект запроса.
        session (Session): Сессия базы данных.
        user_id (int): ID пользователя, которого нужно обновить.
        cur_user_id (int): ID текущего пользователя, выполняющего операцию.
        username (str): Новое имя пользователя.
        user_firstname (str): Новое имя пользователя.
        user_lastname (str): Новая фамилия пользователя.
        is_admin (bool): Новый статус администратора пользователя.

    Возвращаемое значение:
        RedirectResponse: Ответ с редиректом, если обновление прошло успешно.
        JSONResponse: Ответ с сообщением об ошибке, если доступ запрещен.
    """
    user = await UserDAL.get_by_id(user_id, session)
    cur_user = await UserDAL.get_by_id(cur_user_id, session)
    if user and cur_user:
        if cur_user.is_admin:
            user.username = username
            user.first_name = user_firstname
            user.last_name = user_lastname
            user.is_admin = is_admin
            await session.commit()
            url = f'/api/v1/users?cur_user_id={cur_user_id}'
            return RedirectResponse(url=url, status_code=301)
    else:
        return JSONResponse(
            content={'message': 'Access denied'},
            status_code=HTTPStatus.UNAUTHORIZED,
        )
