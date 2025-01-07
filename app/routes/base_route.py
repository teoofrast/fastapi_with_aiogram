# STDLIB
from http import HTTPStatus

# THIRDPARTY
from fastapi import Request
from starlette.responses import JSONResponse
from fastapi.templating import Jinja2Templates

# FIRSTPARTY
from app.DAL.BaseDAL import UserDAL, BaseDAL
from app.database import SessionDep

templates = Jinja2Templates(directory='templates')


async def base_route(request: Request ,inst_dal, cur_user_id, html_temp, session: SessionDep, title):
    cur_user = await UserDAL.get_by_id(cur_user_id, session)
    if cur_user:
        if cur_user.is_admin:
            insts = await inst_dal.get_all(session)
            return templates.TemplateResponse(
                html_temp,
                {
                    'request': request,
                    'title': title,
                    'data': insts,
                    'cur_user_id': cur_user_id,
                },
            )
    else:
        return JSONResponse(
            content={'message': 'Access denied'},
            status_code=HTTPStatus.UNAUTHORIZED,
        )
