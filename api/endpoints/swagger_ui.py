from core.fastapi import FastAPI
# from crud import Session
from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

swagger_ui_router = APIRouter()


@swagger_ui_router.get('/docs', include_in_schema=False)
async def swagger_ui_html(request: Request):
    return get_swagger_ui_html(
        openapi_url=FastAPI().openapi_url,
        title=FastAPI().title,
        oauth2_redirect_url=FastAPI().swagger_ui_oauth2_redirect_url,
    )


@swagger_ui_router.get('/redoc', include_in_schema=False)
async def redoc_html(request: Request):
    return get_redoc_html(
        openapi_url=FastAPI().openapi_url,
        title=FastAPI().title + " - ReDoc",
    )
