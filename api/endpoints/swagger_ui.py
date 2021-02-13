from core.fastapi import FastAPI
from crud.base import Session
from dependencies import set_db_session_in_request
from fastapi import APIRouter, Depends, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

swagger_ui_router = APIRouter()


@swagger_ui_router.get(
    '/docs',
    include_in_schema=False,
    dependencies=[Depends(set_db_session_in_request)])
async def swagger_ui_html(request: Request):
    return get_swagger_ui_html(
        openapi_url=FastAPI().openapi_url,
        title=FastAPI().title,
        oauth2_redirect_url=FastAPI().swagger_ui_oauth2_redirect_url,
    )


@swagger_ui_router.get(
    '/redoc',
    include_in_schema=False,
    dependencies=[Depends(set_db_session_in_request)])
async def redoc_html(request: Request):
    return get_redoc_html(
        openapi_url=FastAPI().openapi_url,
        title=FastAPI().title + " - ReDoc",
    )


def openapi(app: FastAPI, request: Request):
    request.state.db_session = Session

    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI",
        version="0.1.0",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema
