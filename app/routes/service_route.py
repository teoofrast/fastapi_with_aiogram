from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from http import HTTPStatus
from fastapi.responses import JSONResponse

from app.DAL.ServiceDAL import ServiceDAL
from app.models.models import ServiceModel
from tg_bot.settings.settings import BotSettings
from app.database import SessionDep
from app.DAL.BaseDAL import UserDAL


router = APIRouter()

templates = Jinja2Templates(directory="templates")

bot_settings = BotSettings()


@router.get("/api/v1/services")
async def get_services(request: Request, session: SessionDep, cur_user_id: int):
    cur_user = await UserDAL.get_by_id(cur_user_id, session)
    if cur_user:
        if cur_user.is_admin:
            services = await ServiceDAL.get_all(session)
            return templates.TemplateResponse(
                'services.html',
                {
                    "request": request,
                    "title": "Услуги",
                    'services': services,
                    'cur_user_id': cur_user_id})
    else:
        return JSONResponse(content={'message': 'Access denied'}, status_code=HTTPStatus.UNAUTHORIZED)

@router.get("/api/v1/services/add")
async def add_service(request: Request, session: SessionDep, cur_user_id: int):
    return templates.TemplateResponse('service_add.html', {'request': request, 'cur_user_id': cur_user_id})

@router.post("/api/v1/services/add")
async def add_service(
        request: Request,
        session: SessionDep,
        cur_user_id: int,
        service_name: str=Form(...),
        service_cost: int=Form(...),
        service_time: int=Form(...)
):
    cur_user = await UserDAL.get_by_id(cur_user_id, session)
    if cur_user:
        if cur_user.is_admin:
            new_service = ServiceModel(service_name=service_name, service_cost=service_cost, service_time=service_time)
            await ServiceDAL.add_one_service(
                new_service,
                session
            )
            url = f'/api/v1/services?cur_user_id={cur_user_id}'
            return RedirectResponse(url=url, status_code=HTTPStatus.MOVED_PERMANENTLY)
    else:
        return JSONResponse(content={'message': 'Access denied'}, status_code=HTTPStatus.UNAUTHORIZED)