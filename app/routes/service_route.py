"""Маршруты для управления услугами."""

# STDLIB
from http import HTTPStatus

# THIRDPARTY
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse, RedirectResponse

# FIRSTPARTY
from app.DAL.BaseDAL import UserDAL
from app.DAL.ServiceDAL import ServiceDAL
from app.database import SessionDep
from app.models.models import ServiceModel
from tg_bot.settings.settings import BotSettings
from app.routes.base_route import base_route

router = APIRouter()

templates = Jinja2Templates(directory='templates')

bot_settings = BotSettings()


@router.get('/api/v1/services')
async def get_services(
    request: Request, session: SessionDep, cur_user_id: int
):
    """Получает список сервисов для администратора."""
    answer = await base_route(request, ServiceDAL, cur_user_id, 'services.html',session, 'Услуги')
    return answer


@router.get('/api/v1/services/add')
async def add_service(request: Request, session: SessionDep, cur_user_id: int):
    """Отправляет форму для добавления нового сервиса.

    Эта функция обрабатывает GET-запрос для отображения страницы с формой
    для добавления нового сервиса. Доступ к странице имеют пользователи
    с действующими правами доступа.

    Параметры:
        request (Request): Объект запроса для передачи в шаблон.
        session (SessionDep): Сессия базы данных для выполнения запросов.
        cur_user_id (int): ID текущего пользователя, выполняющего запрос.

    Возвращаемое значение:
        TemplateResponse: Возвращает HTML-страницу с формой для добавления
        нового сервиса.
    """
    return templates.TemplateResponse(
        'service_add.html', {'request': request, 'cur_user_id': cur_user_id}
    )


@router.post('/api/v1/services/add')
async def add_one_service(
    request: Request,
    session: SessionDep,
    cur_user_id: int,
    service_name: str = Form(...),
    service_cost: int = Form(...),
    service_time: int = Form(...),
):
    """Добавляет новый сервис для администратора.

    Эта функция обрабатывает POST-запрос для добавления нового сервиса.
    Доступ к добавлению сервисов имеют только пользователи с правами
    администратора. Если текущий пользователь не является администратором,
    возвращается сообщение о запрете доступа. В случае успешного добавления
    нового сервиса происходит перенаправление на список сервисов.

    Параметры:
        request (Request): Объект запроса для передачи в шаблон.
        session (SessionDep): Сессия базы данных для выполнения операций.
        cur_user_id (int): ID текущего пользователя, выполняющего запрос.
        service_name (str): Название нового сервиса.
        service_cost (int): Стоимость нового сервиса.
        service_time (int): Время выполнения нового сервиса.

    Возвращаемое значение:
        Union[JSONResponse, RedirectResponse]: Если текущий юзер является
        администратором, происходит добавление сервиса и перенаправление на
        страницу списка сервисов. В случае отказа в доступе возвращается ответ
        с сообщением о запрете.
    """
    cur_user = await UserDAL.get_by_id(cur_user_id, session)
    if cur_user:
        if cur_user.is_admin:
            new_service = ServiceModel(
                service_name=service_name,
                service_cost=service_cost,
                service_time=service_time,
            )
            await ServiceDAL.add_one_service(new_service, session)
            url = f'/api/v1/services?cur_user_id={cur_user_id}'
            return RedirectResponse(
                url=url, status_code=HTTPStatus.MOVED_PERMANENTLY
            )
    else:
        return JSONResponse(
            content={'message': 'Access denied'},
            status_code=HTTPStatus.UNAUTHORIZED,
        )


@router.get('/api/v1/services/edit/{service_id}')
async def edit_service(
    request: Request, service_id: int, cur_user_id: int, session: SessionDep,
):
    """Страничка для редактирования услуги.

    Параметры:
        request (Request): Объект запроса для передачи в шаблон.
        service_id (int): ID услуги.
        cur_user_id (int): ID текущего пользователя, выполняющего запрос.
        session (SessionDep): Сессия базы данных для выполнения операций.

    Возвращаемое значение:
        templates.TemplateResponse() - html страница с формой редактирования.
        JSONResponse - Ответ с ошибкой для юзера без админ статуса.
    """
    service = await ServiceDAL.get_by_id(service_id, session)
    cur_user = await UserDAL.get_by_id(cur_user_id, session)
    if service and cur_user.is_admin:
        return templates.TemplateResponse(
            'edit_service.html',
            {
                'request': request,
                'title': 'Редактирование услуг',
                'service': service,
                'cur_user_id': cur_user_id,
            },
        )
    else:
        return JSONResponse(
            content={'message': 'Access denied'},
            status_code=HTTPStatus.UNAUTHORIZED,
        )
