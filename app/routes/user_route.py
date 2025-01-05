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

templates = Jinja2Templates(directory="templates")

bot_settings = BotSettings()

@router.post("/api/v1/users")
async def add_user(
        user: UserCreateSchema,
        session: SessionDep
):
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

@router.get("/api/v1/users")
async def get_users(request: Request, session: SessionDep, cur_user_id: int):
    user = await UserDAL.get_by_id(cur_user_id, session)
    if user:
        if user.is_admin:
            users = await UserDAL.get_all(session)
            return templates.TemplateResponse('index.html', {"request": request, "title": "Пользователи", 'users': users, 'cur_user_id': cur_user_id})
    else:
        return JSONResponse(content={'message': 'Access denied'}, status_code=HTTPStatus.FORBIDDEN)


@router.get("/api/v1/users/edit/{user_id}")
async def update_user(request: Request, user_id: int, session: SessionDep, cur_user_id: int):
    user = await UserDAL.get_by_id(user_id, session)
    if user:
        return templates.TemplateResponse(
            'edit_user.html',
            {
                "request": request,
                'title': 'Редактирование пользователя',
                'user': user,
                'cur_user_id': cur_user_id,
            }
        )

@router.post("/api/v1/users/update/{user_id}")
async def update_user(
    request: Request,
    session: SessionDep,
    user_id: int,
    cur_user_id: int,
    username: str=Form(...),
    user_firstname: str=Form(...),
    user_lastname: str=Form(...),
    is_admin: bool=Form(...),
):
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
            status_code=HTTPStatus.UNAUTHORIZED
        )
